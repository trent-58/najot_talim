from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.profile_edit, name="profile-edit"),
    path("change-password", views.change_password, name="change-password"),
    path("categories", views.Categories.as_view(), name="categories"),
    path("category/create", views.CategoryCreateView.as_view(), name="category-create"),
    path("category/<int:pk>/list", views.category_list, name="category-list"),
    path(
        "category/<int:pk>/edit",
        views.CategoryUpdateView.as_view(),
        name="category-edit",
    ),
    path(
        "category/<int:pk>/delete",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
    path("product/<int:pk>", views.product_detail, name="product"),
    path("product/create", views.ProductCreateView.as_view(), name="product-create"),
    path("product/<int:pk>/edit", views.ProductUpdateView.as_view(), name="product-edit"),
    path("product/<int:pk>/delete", views.ProductDeleteView.as_view(), name="product-delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
