
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Books
from .forms import BookForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('book_list') # or wherever
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def book_list(request):
    books = Books.objects.all()
    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'bookapp/book_list1.html', {'page_obj': page_obj})



def book_detail(request, pk):
    book = get_object_or_404(Books, pk=pk)
    return render(request, 'bookapp/book_detail.html', {'book': book})

# @login_required
@user_passes_test(lambda u: u.userprofile.role == 'user' or u.userprofile.role == 'admin')
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookapp/book_form.html', {'form': form})

@user_passes_test(lambda u: u.userprofile.role == 'admin')
def book_update(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookapp/book_form.html', {'form': form})


@user_passes_test(lambda u: u.userprofile.role == 'admin')
def book_delete(request, pk):
    book = get_object_or_404(Books, pk=pk)
    book.delete()
    return redirect('book_list')