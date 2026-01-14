import datetime

from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Author,Book,BookInstance,Genre
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm
from django.contrib.auth.decorators import login_required ,permission_required 

#Function based view
def index(request):
    'View funcrion for home page of the site'

    #Generating count of some main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    #Count of available book instances
    available_instances = BookInstance.objects.filter(status__exact='a').count()

    num_author=Author.objects.count()
    num_genres=Genre.objects.filter(name__contains='Self-Help').count()
    num_books_self_help=Book.objects.filter(summary__contains='Self Help').count()

    num_visits= request.session.get("num_visits",0)
    num_visits+=1
    request.session['num_visits']=num_visits
    context={
        "num_books":num_books,
        "num_instances":num_instances,
        "available_instances":available_instances,
        "num_author":num_author,
        "num_self_help":num_genres,
        "num_books_self_help":num_books_self_help,
        "num_visits":num_visits

    }
    return render(request,'index.html',context=context)


class BookListView(ListView):
    model = Book

    # def getquery_set(self):
    #     return Book.objects.filter(title__icontains='murder')[:5]
   
class BookDetailView(DetailView):
    model=Book

class AuthorListView(ListView):
    model=Author
    
class AuthorDetailView(DetailView):
    model=Author

class BooksLoanedByUser(LoginRequiredMixin,ListView):
    """Generic class based view for listing the book's user have loaned to him/her"""
    model=BookInstance
    # template='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    #In order to restrict our query to just the BookInstance objects for the current user, we re-implement get_queryset()
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back')
        )
    
class AllBooksLoanedByUser(PermissionRequiredMixin,ListView):
    """Generic class based view for listing all books to the librarian with permission to mark book returned"""

    permission_required =['catalog.can_marked_return','catalog.can_renew']
    model=BookInstance
    template_name='catalog/bookinstance_list_all_user.html'
    paginate_by = 10
    #In order to restrict our query to just the BookInstance objects for the current user, we re-implement get_queryset()
    def get_queryset(self):
        return (
            BookInstance.objects
            .filter(status__exact='o')
            .order_by('due_back','borrower')
        )
@login_required 
@permission_required('catalog.can_renew',raise_exception=True)
def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)

    #If post request then process the Form Data
    if request.method =='POST':
        #Create an instance of form and populate it with data from the request(binding)
        form= RenewBookForm(request.POST)

        #checking if the form is valid
        if form.is_valid():
            #process the data in form.cleaned data , here we want to update the model field ;due_back to a new date
            book_instance.due_back=form.cleaned_data['renewal_date']
            book_instance.save()

            # redirecting to the new url ,which is librarian page 
            return HttpResponseRedirect(reverse("all-borrowed"))
    #If the request is GET it means its the first request and return default form 
    else:
        proposed_renewal_date=datetime.date.today() +datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context ={
        'form':form,
        'book_instance':book_instance
    }
    
    return render(request,'catalog/book_renew_librarian.html',context) #if the form is not valid we will render the page and the form context variable will also include error messages


