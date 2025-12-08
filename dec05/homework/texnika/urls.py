from django.urls import path
from .views import (
    index,
    item_list,
    add_item,
    show_item,
    edit_item,
    categories,
    add_category,
    show_category,
    edit_category,
    manufacturers,
    add_manufacturer,
    show_manufacturer,
    edit_manufacturer,
)

urlpatterns = [
    path("", index, name="texnika"),
    # Items
    path("items/", item_list, name="items"),
    path("items/add", add_item, name="add_item"),
    path("items/<int:pk>", show_item, name="show_item"),
    path("items/<int:pk>/edit", edit_item, name="edit_item"),
    # Categories
    path("categories/", categories, name="categories"),
    path("categories/add", add_category, name="add_category"),
    path("categories/<int:pk>", show_category, name="show_category"),
    path("categories/<int:pk>/edit", edit_category, name="edit_category"),
    # Manufacturers
    path("manufacturers/", manufacturers, name="manufacturers"),
    path("manufacturers/add", add_manufacturer, name="add_manufacturer"),
    path("manufacturers/<int:pk>", show_manufacturer, name="show_manufacturer"),
    path("manufacturers/<int:pk>/edit", edit_manufacturer, name="edit_manufacturer"),
]
