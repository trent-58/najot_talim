from rest_framework import serializers
from .models import Income, Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'account', 'category', 'amount', 'note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'account', 'category', 'amount', 'note', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']