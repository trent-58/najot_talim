import random
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.password_validation import validate_password
from django.conf import settings

from baseapp.models import BaseModel


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email or self.phone_number} - {self.user_role}"
        
    def create_code_verification(self, auth_type):
        CodeVerification.objects.filter(
            user=self,
            auth_type=auth_type,
            is_active=True
        ).update(is_active=False)

        code = f"{random.randint(1000, 9999)}"

        CodeVerification.objects.create(
            user=self,
            code=code,
            auth_type=auth_type,
            is_active=True
        )

    def check_username(self):
        if not self.email and not self.phone_number:
            raise ValidationError("User must have either email or phone number")

    def check_email(self):
        if self.auth_type == VIA_EMAIL and not self.email:
            raise ValidationError("Email is required when auth_type is via_email")

    def check_phone(self):
        if self.auth_type == VIA_PHONE and not self.phone_number:
            raise ValidationError("Phone number is required when auth_type is via_phone")

    def check_password(self, raw_password):
        validate_password(raw_password, user=self)

    def hash_password(self, raw_password):
        self.set_password(raw_password)
        
    def clean(self):
        self.check_username()
        self.check_email()
        self.check_phone()

        if self.email and self.phone_number:
            raise ValidationError("User cannot have both email and phone number")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class CodeVerification(BaseModel):
    USER_AUTH_TYPE_CHOICES = (
        (VIA_EMAIL, VIA_EMAIL),
        (VIA_PHONE, VIA_PHONE),
    )

    code = models.CharField(max_length=4)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='code_verifications'
    )
    auth_type = models.CharField(max_length=20, choices=USER_AUTH_TYPE_CHOICES)
    is_active = models.BooleanField(default=False)
    expiry_time = models.DateTimeField()

    def __str__(self):
        return f"CodeVerification for {self.user} via {self.auth_type}"

    def save(self, *args, **kwargs):
        if not self.expiry_time:
            if self.auth_type == VIA_EMAIL:
                minutes = settings.EMAIL_CODE_EXPIRY_MINUTES
            else:
                minutes = settings.PHONE_CODE_EXPIRY_MINUTES

            self.expiry_time = timezone.now() + timedelta(minutes=minutes)

        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expiry_time
