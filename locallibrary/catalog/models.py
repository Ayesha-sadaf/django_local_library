from django.db import models
from django.urls import reverse # To generate URLS by reversing URL patterns
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import User
import uuid
from datetime import date

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(
        max_length=200,
        unique=True, #prevent genre with exactly the same name
        help_text="Enter a book genre(e.g Science,Fiction,Horror etc)"
    )

    def __str__(self):
        "String representation when an instance of Genre is called"
        return self.name
    def get_absolute_url(self):
        return reverse("genre-detail",args=[str(self.id)]) #define url mapping with name genre detail and a view associated with it 
    
    class Meta:
        constraints= [
            UniqueConstraint(
                Lower("name"), #converts anmes to lower cases before checking uniqueness,
                name="genre_name_case_insensitive_unique" , #handles case insesitve duplicates
                violation_error_message="Genre already exists(case insensitive match found)"
            )
        ]


class Book(models.Model):
    """A model representing the book table"""
    title=models.CharField(max_length=200)
    #We are using ForeignKey to map the one-to-many relationship ,we are specifying author as text right now as it hasnt been specified yet
    author = models.ForeignKey("Author",on_delete=models.RESTRICT,null=True) #on_delete=models.Restrict which will prevent the book's associated author being deleted if it is referenced by any book.
    isbn=models.CharField("ISBN", max_length=13,help_text='13 Character')
    summary=models.TextField(max_length=1000,help_text="Enter brief description of the book")

    language=models.ForeignKey("Language",null=True, blank=True ,on_delete=models.SET_NULL)
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail",args=[str(self.id)])

    #creating this display function to add in BookAdmin 
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    #book instance represent physical copy of a book
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text="Unique identifier for this book across the library")
    due_back=models.DateField(null=True,blank=True)
    book=models.ForeignKey(Book,on_delete=models.RESTRICT,null=True) #null=True in developing stage so the instance of book can be added wihtout needing to link with the book
    
    #adding borrower to associate a book with User 
    borrower=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    @property
    def is_overdue(self):
        """Determines if the book is overdue based on due date and current date."""
        return bool(self.due_back and date.today() > self.due_back)


    LOAN_STATUS=(
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status=models.CharField(max_length=1 ,choices=LOAN_STATUS,default='a',help_text="Book availibility")

    class Meta:
        ordering =['status']
        permissions=(('can_marked_return','set book as returned'),('can_renew','change the due back date of book'),) #permission in a tuple with the name and description
    
    def __str__(self):
        return f'{self.id},({self.book.title})'

    #no need for absolute url function as Book have it for showing details of it.

class Author(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    dob= models.DateField(null=True,blank=True)
    dod=models.DateField("Died",null=True,blank=True)

    class Meta:
        ordering = ['first_name','last_name']

    def get_absolute_url(self):
        return reverse("author-detail",args=[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name},{self.last_name}'
    

class Language(models.Model):
    name=models.CharField(
        "Language",
        max_length=200,
        unique=True)
    class Meta:
        constraints=[
            UniqueConstraint(
            Lower("name"),
            name="language_name_case_insensitive_unique" , #handles case insesitve duplicates,
            violation_error_message="Language already exists(case insensitive match found)"
            )
        ]

    def __str__(self):
        return self.name
    