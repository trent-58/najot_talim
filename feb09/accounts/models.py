import random
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from baseapp.models import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


ADMIN, MANAGER, USER = ('admin', 'manager', 'user')
NEW, CODE_VERIFY, DETAILS, PICTURE, DONE = ('new', 'code_verify', 'details', 'picture', 'done')
VIA_EMAIL, VIA_PHONE, VIA_USERNAME = ('via_email', 'via_phone', 'via_username')




class CustomUser(AbstractUser, BaseModel):
    USER_ROLE_CHOICES = ((ADMIN, ADMIN),(MANAGER, MANAGER), (USER, USER),)
    USER_STATUS_CHOICES = ((NEW, NEW), (CODE_VERIFY, CODE_VERIFY), (DETAILS, DETAILS), (PICTURE, PICTURE), (DONE, DONE),)
    USER_AUTH_TYPE_CHOICES = ((VIA_EMAIL, VIA_EMAIL), (VIA_PHONE, VIA_PHONE), (VIA_USERNAME, VIA_USERNAME))
    user_status = models.CharField(max_length=20, choices=USER_STATUS_CHOICES, default=NEW, null=True, blank=True)
    user_role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, default=USER, null=True, blank=True)
    auth_type = models.CharField(max_length=20, choices=USER_AUTH_TYPE_CHOICES, default=VIA_EMAIL, null=True, blank=True)
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to='user_profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.email or self.phone_number or self.username
        
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
        return code

    def check_username(self, username):
        if not username:
            return
        qs = CustomUser.objects.filter(username=username).exclude(pk=self.pk)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Username is already taken")

    def check_email(self, email):
        if not email:
            return
        qs = CustomUser.objects.filter(email=email)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Email is already taken")


    def check_phone(self, phone_number):
        if not phone_number:
            return
        qs = CustomUser.objects.filter(phone_number=phone_number)
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError("Phone number is already taken")

    def validate_raw_password(self, raw_password):
        validate_password(raw_password, user=self)

    def hash_password(self, raw_password):
        self.set_password(raw_password)
        
    def clean(self):
        self.check_username(self.username)
        self.check_email(self.email)
        self.check_phone(self.phone_number)
        if self.email and self.phone_number:
            raise ValidationError("User cannot have both email and phone number")


    def get_tokens(self):

        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }



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
                minutes = settings.EMAIL_EXPIRATION_TIME_MINUTES
            else:
                minutes = settings.PHONE_EXPIRATION_TIME_MINUTES

            self.expiry_time = timezone.now() + timedelta(minutes=minutes)

        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expiry_time
