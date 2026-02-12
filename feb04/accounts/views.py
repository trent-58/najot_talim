from django.views.generic import CreateView

from jan22.users.serializers import SignUpSerializer
from .models import CustomUser

# Create your views here.
class SignUpView(CreateView):
    serializer_class = SignUpSerializer
    queryset = CustomUser.objects.all()