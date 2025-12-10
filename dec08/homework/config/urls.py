from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("food/", include("food_market.urls")),
    path("tour/", include("tour_agency.urls")),
]
