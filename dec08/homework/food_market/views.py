from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "food_market/product_list.html"
    context_object_name = "products"
    paginate_by = 10


class ProductDetailView(DetailView):
    model = Product
    template_name = "food_market/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    template_name = "food_market/product_form.html"
    fields = ["name", "price", "description", "quantity", "category"]
    success_url = reverse_lazy("product_list")


class ProductUpdateView(UpdateView):
    model = Product
    template_name = "food_market/product_form.html"
    fields = ["name", "price", "description", "quantity", "category"]
    success_url = reverse_lazy("product_list")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "food_market/product_confirm_delete.html"
    success_url = reverse_lazy("product_list")
