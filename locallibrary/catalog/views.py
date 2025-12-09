from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Author,Book,BookInstance,Genre

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
    context={
        "num_books":num_books,
        "num_instances":num_instances,
        "available_instances":available_instances,
        "num_author":num_author,
        "num_self_help":num_genres,
        "num_books_self_help":num_books_self_help

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



