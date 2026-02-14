from django.urls import path, include
from .views import RegisterView, CodeVerifyView, GetNewCodeView, RegisterDetailView, UserChangePhotoView, UserView, LoginView, LogoutView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='signup'),
    path('code-verify/', CodeVerifyView.as_view(), name='code_verify'),
    path('getnewcode/', GetNewCodeView.as_view(), name='get-new-code'),
    path('register-detail/', RegisterDetailView.as_view(), name='register-detail'),
    path('update-photo/', UserChangePhotoView.as_view(), name='update-photo'),
    path('user-details/', UserView.as_view(), name='user-details'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
