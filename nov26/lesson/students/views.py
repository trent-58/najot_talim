from django.shortcuts import render
from django.http import HttpResponse


def students(request):
    return HttpResponse("<a href='about/'>About</a> <a href='my_group/'>My group</a>")

def about(request):
    return HttpResponse("About student")

def my_group(request):
    return HttpResponse("My group")

