from django.shortcuts import render
from django.http import HttpResponse

def see_transactions(request):
    return HttpResponse("Here are the transactions")

def see_details(request):
    return HttpResponse("Here are the details")

def index(request):
    return HttpResponse("<a href='see/'>See</a>  |  <a href='details/'>Details</a>")