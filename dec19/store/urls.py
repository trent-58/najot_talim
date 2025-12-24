from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/add/", views.CategoryCreateView.as_view(), name="category_add"),
    path(
        "categories/<int:pk>/edit/",
        views.CategoryUpdateView.as_view(),
        name="category_edit",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "products/category/<int:category_pk>/",
        views.ProductListView.as_view(),
        name="product_list_by_category",
    ),
    path(
        "products/user/<int:user_pk>/",
        views.ProductListView.as_view(),
        name="product_list_by_user",
    ),
    path("products/add/", views.ProductCreateView.as_view(), name="product_add"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"
    ),
    path(
        "products/<int:pk>/edit/",
        views.ProductUpdateView.as_view(),
        name="product_edit",
    ),
    path(
        "products/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="product_delete",
    ),
    path(
        "products/<int:product_pk>/comments/add/",
        views.CommentCreateView.as_view(),
        name="comment_add",
    ),
    path(
        "comments/<int:pk>/edit/",
        views.CommentUpdateView.as_view(),
        name="comment_edit",
    ),
    path(
        "comments/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment_delete",
    ),
]
