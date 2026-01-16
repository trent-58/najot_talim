from rest_framework import serializers
from .models import Account, ExpenseCategory, IncomeCategory


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "user",
            "name",
            "type",
            "currency",
            "balance",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]

    def validate_type(self, value):
        if not value:
            return value
        return str(value).upper()

    def validate_status(self, value):
        if not value:
            return value
        return str(value).upper()


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ["id", "user", "name", "icon", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]


class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ["id", "user", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
