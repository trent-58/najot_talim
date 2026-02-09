from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import (
    CustomUser,
    CodeVerification,
    VIA_EMAIL,
    VIA_PHONE,
    CODE_VERIFY,
)


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = (
            'auth_type',
            'email',
            'phone_number',
            'password',
        )

    def validate_auth_type(self, value):
        if value not in (VIA_EMAIL, VIA_PHONE):
            raise ValidationError("Invalid auth_type")
        return value

    def validate_email(self, value):
        if value and CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Email already exists")
        return value

    def validate_phone_number(self, value):
        if value and CustomUser.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number already exists")
        return value

    def validate(self, attrs):
        auth_type = attrs.get('auth_type')
        email = attrs.get('email')
        phone = attrs.get('phone_number')

        if auth_type == VIA_EMAIL and not email:
            raise ValidationError("Email is required")

        if auth_type == VIA_PHONE and not phone:
            raise ValidationError("Phone number is required")

        if email and phone:
            raise ValidationError("Provide only one of email or phone number")

        user = CustomUser(**attrs)

        try:
            user.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict or e.messages)

        user.check_password(attrs['password'])

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.hash_password(password)
        user.user_status = CODE_VERIFY
        user.save()

        CodeVerification.objects.filter(
            user=user,
            auth_type=user.auth_type,
            is_active=True
        ).update(is_active=False)

        user.create_code_verification(user.auth_type)

        return user


