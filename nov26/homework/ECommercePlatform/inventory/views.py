from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='items/'>Inventory items</a> | <a href='info/'>Inventory Info</a>")

def view_items(request):
    return HttpResponse("Items in the inventory.")

def view_info(request):
    return HttpResponse("Detail of a specific item.")