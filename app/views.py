from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def home(request):
    products = Product.objects.all()
    return render(request, 'shop/home.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    return render(request, 'shop/cart.html', {'items': items})

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if items.exists():
        order = Order.objects.create(user=request.user)
        order.items.set(items)
        order.is_ordered = True
        order.save()
        items.delete()
        return render(request, 'shop/checkout_success.html', {'order': order})
    return redirect('cart')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login_user')
    return render(request, 'shop/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'shop/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
