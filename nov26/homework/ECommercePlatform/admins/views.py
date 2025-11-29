from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='view/'>View Admins</a> | <a href='add/'>Add an admin</a>")

def view_admins(request):
    return HttpResponse("View Admins")

def add_admin(request):
    return HttpResponse("Add Admin")