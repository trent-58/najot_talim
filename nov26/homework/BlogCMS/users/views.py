from django.shortcuts import render
from django.http import HttpResponse

def see_users(request):
    return HttpResponse("you now are seeing users")

def see_info(request):
    return HttpResponse("you are seeing user info")

def index(request):
    text = "<a href='see/'>See users</a>  <a href='info/'>See user info</a>"

    return HttpResponse(text)