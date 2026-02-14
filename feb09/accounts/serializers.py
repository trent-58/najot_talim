from django.db import transaction
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from typing import cast
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import CustomUser, VIA_EMAIL, VIA_PHONE, CODE_VERIFY, DETAILS, PICTURE, DONE, VIA_USERNAME
from .utils import check_if_email_or_phone
from uuid import uuid4
import logging
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.ModelSerializer):
    userinput = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('userinput',)

    def validate_email(self, value):
        if value and CustomUser.objects.filter(email=value).exists():
            raise ValidationError("Email already exists")
        return value

    def validate_phone_number(self, value):
        if value and CustomUser.objects.filter(phone_number=value).exists():
            raise ValidationError("Phone number already exists")
        return value

    def validate(self, attrs):
        userinput = attrs.get('userinput', '').strip()
        attrs.pop('userinput')
        auth_type = check_if_email_or_phone(userinput)
        if not auth_type:
            raise ValidationError("Email or phone number required")

        if VIA_PHONE == auth_type:
            phone = userinput
            self.validate_phone_number(phone)
            attrs.update(phone_number=phone)
        if VIA_EMAIL == auth_type:
            email = userinput
            self.validate_email(email)
            attrs.update(email=email)

        attrs.update(username=str(uuid4()).split('-')[-1], auth_type=auth_type, password=str(uuid4()).split('-')[-1])
        user = CustomUser(**attrs)

        try:
            user.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict or e.messages)
        user.validate_raw_password(attrs['password'])
        attrs.update(is_active=False)
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser(**validated_data)
        user.hash_password(password)
        user.user_status = CODE_VERIFY
        user.save()
        code = user.create_code_verification(user.auth_type)
        if user.auth_type == VIA_EMAIL:
            send_mail(
                subject="Code",
                message=f"Code: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
        elif user.auth_type == VIA_PHONE:
            print(code)
        return user


class CodeVerificationSerializer(serializers.ModelSerializer):
    userinput = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('userinput', 'code')

    def validate(self, attrs):
        userinput = attrs.get('userinput', '').strip()
        code = str(attrs.get('code', '')).strip()
        auth_type = check_if_email_or_phone(userinput)
        if not auth_type:
            raise ValidationError("Email or phone number required")
        if not code:
            raise ValidationError("Code is required")
        attrs.pop('userinput')
        if VIA_PHONE == auth_type:
            user = CustomUser.objects.filter(phone_number=userinput).first()
        else:
            user = CustomUser.objects.filter(email=userinput).first()
        if not user:
            raise ValidationError("User not found")
        if user.user_status != CODE_VERIFY:
            raise ValidationError("Unexpected status code")

        verification = (
            user.code_verifications
            .filter(auth_type=auth_type, is_active=True)
            .order_by('-created_at')
            .first()
        )
        if not verification:
            raise ValidationError("Code was not found")
        if verification.is_expired():
            verification.is_active = False
            verification.save(update_fields=['is_active'])
            raise ValidationError("Code expired")
        if code != str(verification.code):
            raise ValidationError("Code sent was not valid")

        attrs['user'] = user
        attrs['verification'] = verification
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = validated_data['user']
        verification = validated_data['verification']
        verification.is_active = False
        verification.save(update_fields=['is_active'])
        user.is_active = True
        user.user_status = DETAILS
        user.save(update_fields=['user_status', 'is_active'])
        tokens = user.get_tokens()
        return tokens


class RegisterDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "username", 'password')

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        setattr(instance, 'is_active', True)
        setattr(instance, 'user_status', PICTURE)

        if password:
            validate_password(password, user=instance)
            instance.set_password(password)
        instance.save()
        return instance


class UserChangePhotoSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField

    class Meta:
        model = CustomUser
        fields = ('photo',)

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.photo = photo
            instance.user_status = DONE
            instance.save()
            return instance


class RetrieveUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'auth_type', 'user_status', 'user_role', 'is_staff', 'is_active', 'is_superuser', 'photo')


class LoginSerializer(serializers.ModelSerializer):
    userinput = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('userinput', 'password')

    def save(self, **kwargs):
        userinput = self.validated_data.get('userinput', '').strip()
        password = self.validated_data.get('password', '')

        auth_type = check_if_email_or_phone(userinput)
        logger.info("Login attempt", extra={"auth_type": auth_type})
        if not auth_type:
            raise ValidationError("Email or phone number required")

        found_user = None
        if auth_type == VIA_PHONE:
            logger.info("Authenticating via phone")
            found_user = CustomUser.objects.filter(phone_number=userinput).first()
            if not found_user:
                raise ValidationError("User not found")
        elif auth_type == VIA_EMAIL:
            logger.info("Authenticating via email")
            found_user = CustomUser.objects.filter(email=userinput).first()
            if not found_user:
                raise ValidationError("User not found")
        else:
            logger.info("Authenticating via username")
            found_user = CustomUser.objects.filter(username=userinput).first()
            if not found_user:
                raise ValidationError("User not found")

        user = authenticate(username=found_user.username, password=password)

        if not user:
            logger.warning("Authentication failed for existing user")
            raise ValidationError("Invalid credentials")

        logger.info("Authentication successful")
        user = cast(CustomUser, user)
        tokens = user.get_tokens()
        return tokens


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    default_error_messages = {
        "bad_token": "Token is invalid or expired",
    }

    def validate(self, attrs):
        refresh = attrs.get("refresh")

        try:
            RefreshToken(refresh)
        except TokenError:
            self.fail("bad_token")

        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.validated_data["refresh"])
            token.blacklist()
        except TokenError:
            self.fail("bad_token")
