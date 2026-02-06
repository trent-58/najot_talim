from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from baseapp.models import BaseModel
from datetime import datetime, timedelta
from django.conf.settings import EMAIL_CODE_EXPIRY_MINUTES, PHONE_CODE_EXPIRY_MINUTES


ADMIN, MANAGER, USER = ('admin', 'manager', 'user')
NEW, CODE_VERIFY, DETAILS, PICTURE = ('new', 'code_verify', 'details', 'picture')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')

class CustomUser(AbstractBaseUser, BaseModel):
    USER_ROLE_CHOICES = (
        (ADMIN, ADMIN),
        (MANAGER, MANAGER),
        (USER, USER),
    )

    USER_STATUS_CHOICES = (
        (NEW, NEW),
        (CODE_VERIFY, CODE_VERIFY),
        (DETAILS, DETAILS),
        (PICTURE, PICTURE),
    )

    USER_AUTH_TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default=USER)
    user_status = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default=NEW)
    auth_type = models.CharField(max_length=20, choices=USER_AUTH_TYPE_CHOICES, default=VIA_EMAIL)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='user_profile_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.email or self.phone_number} - {self.user_role}"

    def create_code_verification(self, auth_type):
        code = "".join([str(random.randint(1000))[-1] for _ in range(4)])
        CodeVerification.objects.create(user=self, code=code, auth_type=auth_type)

    def check_username(self):
        pass

    def check_email(self):
        pass

    def check_phone(self):
        pass

    def check_password(self):
        pass

    def hash_password(self):
        pass


    def clean(self):
        pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class CodeVerification(BaseModel):
    USER_AUTH_TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )
    code = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='code_verifications')
    auth_type = models.CharField(max_length=20, choices=USER_AUTH_TYPE_CHOICES, default=VIA_EMAIL)
    is_active = models.BooleanField(default=False)
    expiry_time = models.DateTimeField()


    def __str__(self):
        return f"CodeVerification for {self.user} via {self.auth_type}"

    def save(self, *args, **kwargs):
        if self.auth_type == VIA_EMAIL:
            self.expiry_time = datetime.now() + timedelta(minutes=EMAIL_CODE_EXPIRY_MINUTES)
        elif self.auth_type == VIA_PHONE:
            self.expiry_time = datetime.now() + timedelta(minutes=PHONE_CODE_EXPIRY_MINUTES)
        super().save(*args, **kwargs)


