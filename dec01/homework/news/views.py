from django.shortcuts import render
from .models import category, news

def index(request):
    categories = category.objects.all()
    context = {'categories': categories}
    return render(request, 'news/index.html', context)

def category_news(request, category_id):
    cat = category.objects.get(id=category_id)
    news_items = news.objects.filter(category_fk=cat)
    context = {'category': cat, 'news_items': news_items}
    return render(request, 'news/category_news.html', context)
