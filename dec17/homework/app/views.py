from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from . import models
from . import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


def get_categories_for_header():
    categories = cache.get("header_categories")
    if categories is None:
        categories = models.Category.objects.all()
        cache.set("header_categories", categories, 60 * 60)
    return categories


def home(request):
    categories = get_categories_for_header()
    products = models.Product.objects.all()[:12]

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "products": products,
            "user": request.user,
        },
    )


def product_detail(request, pk):
    categories = get_categories_for_header()
    product = get_object_or_404(models.Product, pk=pk)

    return render(
        request,
        "product.html",
        {
            "categories": categories,
            "product": product,
            "user": request.user,
        },
    )


def category_list(request, pk):
    categories = get_categories_for_header()
    category = get_object_or_404(models.Category, pk=pk)
    products = category.products.all()

    return render(
        request,
        "category.html",
        {"categories": categories, "products": products, "user": request.user},
    )


class Categories(ListView):
    model = models.Category
    template_name = "categories.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Category
    form_class = forms.CategoryForm
    template_name = "category_form.html"
    success_url = reverse_lazy("categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Category
    template_name = "category_confirm_delete.html"
    success_url = reverse_lazy("categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = models.Product
    form_class = forms.ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Product
    form_class = forms.ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header_categories'] = get_categories_for_header()
        return context


def register(request):
    categories = get_categories_for_header()
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = forms.RegisterForm()

    return render(
        request,
        "register.html",
        {"form": form, "categories": categories}
    )


def login_view(request):
    categories = get_categories_for_header()
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = forms.LoginForm()

    return render(
        request,
        "login.html",
        {"form": form, "categories": categories}
    )


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def profile(request):
    categories = get_categories_for_header()
    return render(
        request,
        "profile.html",
        {"categories": categories, "user": request.user}
    )


@login_required(login_url="login")
def profile_edit(request):
    categories = get_categories_for_header()
    if request.method == "POST":
        form = forms.UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = forms.UserUpdateForm(instance=request.user)

    return render(
        request,
        "profile_edit.html",
        {"form": form, "categories": categories}
    )


@login_required(login_url="login")
def change_password(request):
    categories = get_categories_for_header()
    if request.method == "POST":
        form = forms.PasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data["current_password"]
            new_password = form.cleaned_data["new_password"]

            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                return redirect("profile")
            else:
                form.add_error("current_password", "Current password is incorrect")
    else:
        form = forms.PasswordChangeForm()

    return render(
        request,
        "change_password.html",
        {"form": form, "categories": categories}
    )
