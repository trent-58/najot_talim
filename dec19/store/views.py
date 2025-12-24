from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Category, Product, Comment
from .forms import ProductForm, CategoryForm, CommentForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


User = get_user_model()


def home(request):
    from .models import Product

    recommended = Product.objects.all()[:6]
    from django.shortcuts import render

    return render(request, "home.html", {"recommended": recommended})


class CategoryListView(generic.ListView):
    model = Category
    template_name = "store/category_list.html"


class CategoryCreateView(generic.CreateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    model = Category
    form_class = CategoryForm
    template_name = "store/category_form.html"
    success_url = reverse_lazy("store:category_list")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(generic.UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    model = Category
    form_class = CategoryForm
    template_name = "store/category_form.html"
    success_url = reverse_lazy("store:category_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied("You cannot edit categories you did not create.")
        return obj


class CategoryDeleteView(generic.DeleteView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    model = Category
    template_name = "store/category_confirm_delete.html"
    success_url = reverse_lazy("store:category_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied("You cannot delete categories you did not create.")
        return obj


class ProductListView(generic.ListView):
    model = Product
    template_name = "store/product_list.html"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related("category", "created_by")
        category_pk = self.kwargs.get("category_pk")
        user_pk = self.kwargs.get("user_pk")
        if category_pk:
            category = get_object_or_404(Category, pk=category_pk)
            return qs.filter(category=category)
        if user_pk:
            user = get_object_or_404(User, pk=user_pk)
            return qs.filter(created_by=user)
        return qs


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "store/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["other_products"] = Product.objects.filter(
            category=product.category
        ).exclude(pk=product.pk)[:5]
        return context


class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "store/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product_pk = self.kwargs.get("product_pk")
        product = get_object_or_404(Product, pk=product_pk)
        return redirect(product.get_absolute_url())

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        product_pk = self.kwargs.get("product_pk")
        product = get_object_or_404(Product, pk=product_pk)
        form.instance.product = product
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_pk = self.kwargs.get("product_pk")
        context["product"] = get_object_or_404(Product, pk=product_pk)
        return context

    def get_success_url(self):
        return self.object.product.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "store/comment_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        from .models import Comment

        obj = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        if obj.author != self.request.user:
            raise PermissionDenied("You cannot edit comments you did not create.")
        return obj

    def get_success_url(self):
        return self.object.product.get_absolute_url()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        return redirect(obj.product.get_absolute_url())


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment
    template_name = "store/comment_confirm_delete.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        from .models import Comment

        obj = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        if obj.author != self.request.user:
            raise PermissionDenied("You cannot delete comments you did not create.")
        return obj

    def get_success_url(self):
        return self.object.product.get_absolute_url()

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        return redirect(obj.product.get_absolute_url())


class ProductCreateView(generic.CreateView):
    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProductUpdateView(generic.UpdateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    model = Product
    form_class = ProductForm
    template_name = "store/product_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied("You cannot edit products you did not create.")
        return obj


class ProductDeleteView(generic.DeleteView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login

            return redirect_to_login(request.get_full_path())
        return super().dispatch(request, *args, **kwargs)

    model = Product
    template_name = "store/product_confirm_delete.html"
    success_url = reverse_lazy("store:product_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied("You cannot delete products you did not create.")
        return obj
