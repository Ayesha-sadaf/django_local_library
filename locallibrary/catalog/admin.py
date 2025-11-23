# Register your models here.
from django.contrib import admin
from .models import Genre,Author,Book,BookInstance ,Language


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class BookAdmin(admin.ModelAdmin):
    list_display=['title','author','display_genre']
    inlines = [BooksInstanceInline]
admin.site.register(Book , BookAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=['book','id','status','due_back']
    list_filter =['status','due_back']
    fieldsets = [('None',{'fields':('book','id')}),
                 ('Availability',{'fields':('status','due_back')})]
   
    
class BookInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'dob', 'dod']
    inlines=[BookInline]

admin.site.register(Genre)
admin.site.register(Language)

