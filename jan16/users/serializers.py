from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .utils import validate_phone
import re

class SignUpSerializers(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['first_name', 'last_name', 'username', 'password', 'phone', 'address']
    extra_kwargs = {
        'password': {'write_only': True}
    }

  @staticmethod
  def auth_validate(data):
    phone = data.get('phone', None)
    if not phone: raise ValidationError({'phone': "This field is required."})
    validate_phone(phone)


  def validate(self, data):
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$')
    self.auth_validate(data)
    password = data.get('password', None)
    if password is None:
      raise ValidationError()
    elif not (7 <= len(password) <= 20):
      raise ValidationError('Password must be between 7 and 20 characters')
    elif not password_regex.match(password):
      raise ValidationError('Password must contain at least one uppercase letter, one lowercase letter, and one digit and one special character')
    return data




  def create(self, validated_data):
    user = CustomUser.objects.create_user(**validated_data)
    return user

  def to_representation(self, instance):
    if isinstance(instance, CustomUser):
      token, _ = Token.objects.get_or_create(user=instance)
      return {
        'status': status.HTTP_201_CREATED,
        'token': token.key,
        'username': instance.username,
      }
    return super().to_representation(instance)
