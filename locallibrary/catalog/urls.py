from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/',views.BookListView.as_view(),name='book'),
    #we must use pk for primary key as it is expected by our view classes
    path('books/<int:pk>',views.BookDetailView.as_view() ,name="book-detail"),
    path('authors/',views.AuthorListView.as_view(),name='authors'),
    path('authors/<int:pk>',views.AuthorDetailView.as_view(),name='author-detail'),
    path('mybooks/',views.BooksLoanedByUser.as_view(),name='my-borrowed'),
    path('allbooksloaned/',views.AllBooksLoanedByUser.as_view(),name='all-borrowed'),
    #our book instance primary key is uuid thats why we <uuid:pk> as its a string
    path('book/<uuid:pk>/renew/',views.renew_book_librarian ,name='renew-book-librarian'),
    path('author/create',views.AuthorCreate.as_view(),name='author-create'),
    path('author/<int:pk>/update',views.AuthorUpdate.as_view(),name='author-update'),
    path('author/<int:pk>/delete',views.AuthorDelete.as_view(),name='author-delete'),
    path('book/create',views.BookCreate.as_view(),name='book-create'),
    path('book/<int:pk>/update',views.BookUpdate.as_view(),name='book-update'),
    path('book/<int:pk>/delete',views.BookDelete.as_view(),name='book-delete'),
    path('book/<uuid:pk>/borrow/',views.BorrowBook.as_view(),name='borrow-book')
]