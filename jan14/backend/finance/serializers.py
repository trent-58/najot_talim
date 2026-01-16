from rest_framework import serializers
from .models import Expense, Income
from accounts.models import ExpenseCategory, IncomeCategory


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    note = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Expense
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=IncomeCategory.objects.all(),
        required=False,
        allow_null=True,
    )
    note = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Income
        fields = "__all__"
