from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='see/'>See</a>  |  <a href='details/'>Details</a>")

def see(request):
    return HttpResponse("See")

def details(request):
    return HttpResponse("Details")
