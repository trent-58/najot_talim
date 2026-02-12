from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductListCreateAPIView.as_view(), name="product_list_create"),
    path("search/", views.ProductSearchAPIView.as_view(), name="product_search"),
    path("comments/", views.CommentsListAPIView.as_view(), name="comment_list"),
    path("<int:pk>/comments/", views.ProductCommentsListCreateAPIView.as_view(), name="product_comments"),
    path("<int:pk>/", views.ProductDetailAPIView.as_view(), name="product_detail"),
    path("comments/<int:pk>/", views.CommentDetailAPIView.as_view(), name="comment_detail"),
]