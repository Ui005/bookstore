
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Books
from .forms import BookForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem
from .forms import ProfileForm, CheckoutForm
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




@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'shop/profile.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Books, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('book_list')
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cart_items = Cart.objects.filter(user=request.user)
            total_price = sum(item.total_price() for item in cart_items)
            order = Order.objects.create(user=request.user, total_price=total_price)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart_items.delete()
            return redirect('orders')
    else:
        form = CheckoutForm()
    return render(request, 'shop/checkout.html', {'form': form})

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/orders.html', {'orders': orders})


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')
