from django.shortcuts import render, redirect
from .models import Item, Category, Manufacturer
from django import forms


# ============== CATEGORY FORMS ==============
class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["title"]


# ============== MANUFACTURER FORMS ==============
class AddManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ["name", "country"]


# ============== ITEM FORMS ==============
class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description", "image", "category_fk", "manufacturer_fk"]


# ============== MAIN INDEX ==============
def index(request):
    items = [
        {
            "name": "Items",
            "path": "items/",
        },
        {
            "name": "Categories",
            "path": "categories/",
        },
        {
            "name": "Manufacturers",
            "path": "manufacturers/",
        },
    ]
    return render(
        request, "index.html", {"items": items, "title": "Texnika Management"}
    )


# ============== ITEMS CRUD ==============
def item_list(request):
    items = Item.objects.all()
    return render(
        request,
        "list.html",
        {"items": items, "title": "Items", "back": "texnika", "add": "Add Item"},
    )


def add_item(request):
    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            return redirect("show_item", pk=item.pk)
    else:
        form = AddItemForm()

    return render(
        request, "add.html", {"form": form, "title": "Add Item", "back": "items"}
    )


def show_item(request, pk):
    item = Item.objects.get(pk=pk)

    if request.method == "POST":
        item.delete()
        return redirect("items")

    return render(request, "show_item.html", {"item": item, "back": "items"})


def edit_item(request, pk):
    item = Item.objects.get(pk=pk)

    if request.method == "POST":
        form = AddItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect("show_item", pk=item.pk)
    else:
        form = AddItemForm(instance=item)

    return render(
        request, "add.html", {"form": form, "title": "Edit Item", "back": "items"}
    )


# ============== CATEGORIES CRUD ==============
def categories(request):
    items = Category.objects.all()
    return render(
        request,
        "list.html",
        {
            "items": items,
            "title": "Categories",
            "back": "texnika",
            "add": "Add Category",
        },
    )


def add_category(request):
    if request.method == "POST":
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect("show_category", pk=category.pk)
    else:
        form = AddCategoryForm()

    return render(
        request,
        "add.html",
        {"form": form, "title": "Add Category", "back": "categories"},
    )


def show_category(request, pk):
    category = Category.objects.get(pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("categories")

    return render(
        request, "show_category.html", {"category": category, "back": "categories"}
    )


def edit_category(request, pk):
    category = Category.objects.get(pk=pk)

    if request.method == "POST":
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("show_category", pk=category.pk)
    else:
        form = AddCategoryForm(instance=category)

    return render(
        request,
        "add.html",
        {"form": form, "title": "Edit Category", "back": "categories"},
    )


# ============== MANUFACTURERS CRUD ==============
def manufacturers(request):
    items = Manufacturer.objects.all()
    return render(
        request,
        "list.html",
        {
            "items": items,
            "title": "Manufacturers",
            "back": "texnika",
            "add": "Add Manufacturer",
        },
    )


def add_manufacturer(request):
    if request.method == "POST":
        form = AddManufacturerForm(request.POST)
        if form.is_valid():
            manufacturer = form.save()
            return redirect("show_manufacturer", pk=manufacturer.pk)
    else:
        form = AddManufacturerForm()

    return render(
        request,
        "add.html",
        {"form": form, "title": "Add Manufacturer", "back": "manufacturers"},
    )


def show_manufacturer(request, pk):
    manufacturer = Manufacturer.objects.get(pk=pk)

    if request.method == "POST":
        manufacturer.delete()
        return redirect("manufacturers")

    return render(
        request,
        "show_manufacturer.html",
        {"manufacturer": manufacturer, "back": "manufacturers"},
    )


def edit_manufacturer(request, pk):
    manufacturer = Manufacturer.objects.get(pk=pk)

    if request.method == "POST":
        form = AddManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            form.save()
            return redirect("show_manufacturer", pk=manufacturer.pk)
    else:
        form = AddManufacturerForm(instance=manufacturer)

    return render(
        request,
        "add.html",
        {"form": form, "title": "Edit Manufacturer", "back": "manufacturers"},
    )
