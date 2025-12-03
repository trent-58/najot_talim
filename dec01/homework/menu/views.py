from django.shortcuts import render
from .models import category, meal

def index(request):
    categories = category.objects.all()
    context = {'categories': categories}
    return render(request, 'menu/index.html', context)

def category_detail(request, category_id):
    cat = category.objects.get(id=category_id)
    meals = meal.objects.filter(category_fk=cat)
    context = {'category': cat, 'meals': meals}
    return render(request, 'menu/category_detail.html', context)
