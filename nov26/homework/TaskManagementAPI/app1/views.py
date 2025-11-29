from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='see/'>See</a>  |  <a href='details/'>Details</a>")

def see(request):
    return HttpResponse("View")

def details(request):
    return HttpResponse("Info")
