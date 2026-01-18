import re
from rest_framework.exceptions import ValidationError


def validate_phone(phone):
  phone_regex = re.compile(r'^(?:\+?998|0)?[-\s]?(?:\d{2})[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}$')
  if not re.fullmatch(phone_regex, phone):
    data = {
      'success': False,
      'message': 'Phone number is invalid'
      }
    raise ValidationError(data)
  return True