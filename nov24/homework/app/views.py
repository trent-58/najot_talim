from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("Hello")

def hello_world(request):
    return HttpResponse("Hello World")

def greet(request, name):
    return HttpResponse(f"Hello, {name}")

def get_squared(request):
    num = int(request.GET.get('n', 1))
    return HttpResponse(f"{num} squared is {num**2}")

def max_func(request):
    a = int(request.GET.get('a', 1))
    b = int(request.GET.get('b', 1))
    maxNum = max(a, b)
    return HttpResponse(f"Max number is {maxNum}")

def age(request, num):
    if num < 0:
        return HttpResponse(f"Sorry, {num} is negative")
    return HttpResponse(f"Voyaga yetgan. yosh - {num}" if num>=18 else f"Voyaga yetmagan. yosh - {num}")