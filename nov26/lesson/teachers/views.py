from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("<a href='teacher'>Teacher</a>    <a href='teacher2'>Teacher 2</a>")

def teacher(request):
    return HttpResponse("teacher1")

def teacher2(request):
    return HttpResponse("teacher2")