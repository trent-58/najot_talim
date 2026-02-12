from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello.as_view(), name ='hello'),
    path('register/', views.RegisterView.as_view(), name ='register'),
    path('login/', views.LoginAPIView.as_view(), name ='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateAPIView.as_view(), name='profile_update'),
    path('profile/reset-pass/', views.PasswordResetAPIView.as_view(), name='profile_reset_password'),
]
