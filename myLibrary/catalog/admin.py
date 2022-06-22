from django.contrib import admin
from . models import Author, Genre, Book, BookInstance

# Register your models here.
# use the nodek class to change how model are dispalyed in the admin site using the ModelClass class
# Define the model class for Author model
class BookInline(admin.StackedInline):
    model = Book
    extra = 0
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # pass is used when the class is empty
    # list_display  adds addittional fields to the viewws
    list_display = ('first_name','last_name','date_of_birth','date_of_birth')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
# Register the Model Admin with the model Author
# admin.site.register(Author, AuthorAdmin)
# BookInstance admin class
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','status','borrower','due_back',"id")
    list_filter = ('status', 'due_back')
      # The fieldsets attribute is used to group related model information
    # "Availability" is used as the section title and None for none section title
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin class for Book Model using @register decorator 
# @register is the same as => admin.site.register
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BooksInstanceInline]
# Register the Admin class for BookInstance using decorator
# @admin.register(BookInstance)
# class BookInstanceAdmin(admin.ModelAdmin):
#     list_filter = ('status','due_back')
    

# registering the Genre Model
admin.site.register(Genre)
