from django import forms
from .models import Product, Category, Comment


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "category", "image"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text", "rating", "image"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
        }
