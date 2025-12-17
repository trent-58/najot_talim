from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Category, Product
from .forms import CategoryForm, ProductForm


def home(request):
    q = request.GET.get("q", "").strip()
    products = Product.objects.all()
    if q:
        products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
    products = products.order_by("-created_at")[:12]
    context = {
        "latest_products": products,
        "search_query": q,
    }
    return render(request, "shop/home.html", context)


def category_detail(request, pk: int):
    category = get_object_or_404(Category, pk=pk)
    products = category.products.all().order_by("-created_at")
    # Get suggested products from other categories (excluding current category)
    suggested_products = Product.objects.exclude(category=category).order_by("-created_at")[:6]
    return render(request, "shop/category_detail.html", {
        "category": category,
        "products": products,
        "suggested_products": suggested_products
    })


def product_detail(request, pk: int):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})


# Public CRUD: Categories
class CategoryListView(ListView):
    model = Category
    template_name = "shop/category_list.html"
    context_object_name = "categories"


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "shop/category_form.html"
    success_url = reverse_lazy("shop:category_list")


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "shop/category_form.html"
    success_url = reverse_lazy("shop:category_list")


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "shop/category_confirm_delete.html"
    success_url = reverse_lazy("shop:category_list")


# Public CRUD: Products
class ProductListView(ListView):
    model = Product
    template_name = "shop/product_list.html"
    context_object_name = "products"
    paginate_by = 20


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_form.html"
    success_url = reverse_lazy("shop:product_list")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "shop/product_form.html"
    success_url = reverse_lazy("shop:product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "shop/product_confirm_delete.html"
    success_url = reverse_lazy("shop:product_list")
