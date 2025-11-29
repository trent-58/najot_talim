
from django.contrib import admin
from django.urls import include, path
def landing_page(request):
    from django.http import HttpResponse
    text = "<a href='transactions/'>Transactions</a>  | <a href='savings/'>Savings</a> | <a href='checkings/'>Checkings</a>"
    return HttpResponse(text)


urlpatterns = [
    path('', landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('transactions/', include('transactions.urls')),
    path('savings/', include('savings.urls')),
    path('checkings/', include('checkings.urls')),
]