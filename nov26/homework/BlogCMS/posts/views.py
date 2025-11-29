from django.shortcuts import render
from django.http import HttpResponse

def see_post(request):
    return HttpResponse("seeing posts")

def see_detail(request):
    return HttpResponse("seeing details")

def index(request):
    text = "<a href='see/'>See posts</a>  <a href='details/'>details</a>"

    return HttpResponse(text)