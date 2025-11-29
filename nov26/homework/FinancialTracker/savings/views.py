from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return HttpResponse("<a href='see/'>See</a>  |   <a href='details/'>Details</a>")

def see_savings(request):
    return HttpResponse("Here are the savings")

def see_details(request):
    return HttpResponse("Here are the details")