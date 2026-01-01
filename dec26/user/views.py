from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import render

from shop import models as shop_models
from . import forms


def register(request):
    """CREATE - Register new user"""
    categories = shop_models.Category.objects.all()
    if request.user.is_authenticated:
        return redirect('user:detail')

    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('home')
    else:
        form = forms.UserForm()
    return render(request, 'register.html', {'form': form, 'categories': categories})


def login_view(request):
    categories = shop_models.Category.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html', {'categories': categories})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


@login_required(login_url='user:login')
def detail(request):
    """READ - View user profile"""
    categories = shop_models.Category.objects.all()
    user = request.user
    return render(request, 'account.html', {'categories': categories, 'user': user})


@login_required(login_url='user:login')
def orders(request):
    """VIEW - Display user's orders"""
    from cart.models import Order
    categories = shop_models.Category.objects.all()
    user_orders = Order.objects.filter(user=request.user).prefetch_related('items__product')
    return render(request, 'orders.html', {
        'categories': categories,
        'orders': user_orders
    })


@login_required(login_url='user:login')
def edit(request):
    """UPDATE - Edit user profile"""
    categories = shop_models.Category.objects.all()
    user = request.user

    if request.method == 'POST':
        form = forms.UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user:detail')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = forms.UserUpdateForm(instance=user)

    return render(request, 'account_edit.html', {'categories': categories, 'form': form, 'user': user})


@login_required(login_url='user:login')
def delete(request):
    """DELETE - Delete user account"""
    categories = shop_models.Category.objects.all()

    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)

        if user is not None:
            user.delete()
            messages.success(request, 'Your account has been deleted successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password. Account not deleted.')

    return render(request, 'account_delete.html', {'categories': categories})
