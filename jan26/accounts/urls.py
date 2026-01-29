from django.urls import path
from .views import RegisterView, MeView

urlpatterns = [
    path('auth/register/', RegisterView.as_view()),
    path('auth/me/', MeView.as_view()),
]
