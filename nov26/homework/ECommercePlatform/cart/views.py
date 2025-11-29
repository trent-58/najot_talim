from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='items/'>Cart items</a> | <a href='info/'>Cart Info</a>")

def view_items(request):
    return HttpResponse("Here are the items in your cart.")

def view_info(request):
    return HttpResponse("here is detailed information about your cart.")
