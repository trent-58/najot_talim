from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.http import Http404
from django.core.exceptions import PermissionDenied
from .forms import SimpleUserCreateForm, SimpleUserUpdateForm
from store.models import Product, Comment
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


class UserListView(generic.ListView):
    model = User
    template_name = "users/user_list.html"


class UserDetailView(generic.DetailView):
    model = User
    template_name = "users/user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context["products"] = Product.objects.filter(created_by=user)
        context["comments"] = Comment.objects.filter(author=user)
        return context


class UserCreateView(generic.CreateView):
    model = User
    form_class = SimpleUserCreateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = SimpleUserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:user_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404("You cannot edit other users' accounts.")
        return obj


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied("You cannot delete other users' accounts.")
        return obj
