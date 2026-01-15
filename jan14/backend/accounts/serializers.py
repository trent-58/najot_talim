from rest_framework import serializers
from .models import Account, ExpenseCategory, IncomeCategory

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'name', 'type', 'currency', 'balance', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user']

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = ['id', 'user', 'name', 'icon', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user']

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        fields = ['id', 'user', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user']