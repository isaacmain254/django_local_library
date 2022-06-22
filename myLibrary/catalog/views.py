from ast import Delete
from django.shortcuts import render,get_object_or_404
from django.views import generic
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.forms import RenewBookForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView,DeleteView, UpdateView

import datetime
# Create your views here.
@login_required
def index(request):
    # View function for the home page of the site
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available boks with (status= "a")
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    # The all() is implied by default
    num_authors = Author.objects.count()
    # generating count for genre and books that contains certain words(case insensitive)
    num_genres = Genre.objects.all().count()
    certain_words_books = Book.objects.filter(title__icontains='programming').count()
    # implement a session cookie
    # Number of visits to this view as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    
    context = {
        'num_books' : num_books,
        'num_instances': num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_genres' :  num_genres,
        'certain_words_books':  certain_words_books,
        'num_visits' : num_visits,
    }
    # Rendering the html template index.html with data fin the context variable
    return render(request, 'index.html', context= context)

    # using class based views
class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'   # your own name for the list as a template variable
   # queryset = Book.objects.filter(title__icontains='programming')[:5] # Get 5 books containing the title war
    template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
# BookDetailView
class BookDetailView(generic.DetailView):
    model = Book

# Authors ListViews
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class based view list books on loan to current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = 'o').order_by('due_back')



@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


    # generic editing views
    # generic editing views helps edit ,create and update django forms based on models
class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name', "date_of_birth", 'date_of_death']
    initial = {'date_of_death':'11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author 
    fields = '__all__'

class AuthorDelete(DeleteView):
    model  = Author
    success_url = reverse_lazy('authors')


# Generic editing views for creating, editing and deleting books from the model
class BookCreate(CreateView):
    model = Book
    fields = ['title','author', 'summary','isbn','genre']

class BookUpdate(UpdateView):
    model = Book
    fiels = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

