from django.http import HttpResponse

def index(request):
    return HttpResponse("<a href='see/'>See Reciepts</a>  |  <a href='details/'> See Details</a>")

def see(request):
    return HttpResponse("Seeing receipts")

def details(request):
    return HttpResponse("Details details")
