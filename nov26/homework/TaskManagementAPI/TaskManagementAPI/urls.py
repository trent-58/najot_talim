
from django.contrib import admin
from django.urls import include, path

def landing_page(request):
    from django.http import HttpResponse
    text = "<a href='app1/'>App1</a>  | <a href='app2/'>App2</a> | <a href='app3/'>App3</a>"
    return HttpResponse(text)


urlpatterns = [
    path('', landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('app1/', include('app1.urls')),
    path('app2/', include('app2.urls')),
    path('app3/', include('app3.urls')),
]