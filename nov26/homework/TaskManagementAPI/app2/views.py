from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='view/'>See</a>  |  <a href='info/'>Details</a>")

def see(request):
    return HttpResponse("See")

def details(request):
    return HttpResponse("Details")
