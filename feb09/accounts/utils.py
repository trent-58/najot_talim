import re
from .models import VIA_EMAIL, VIA_PHONE, VIA_USERNAME

email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
phone_regex = "^\+?998\s?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$"

def check_if_email_or_phone(value):
    if re.fullmatch(email_regex, value):
        return VIA_EMAIL
    elif re.fullmatch(phone_regex, value):
        return VIA_PHONE
    elif value:
        return VIA_USERNAME
    else:
        return None