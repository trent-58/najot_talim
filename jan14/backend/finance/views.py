from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db import transaction

from .models import Expense, Income
from .serializers import ExpenseSerializer, IncomeSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(account__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        account = serializer.validated_data["account"]
        category = serializer.validated_data.get("category")
        amount = serializer.validated_data["amount"]

        if account.user != self.request.user:
            raise PermissionDenied("Account does not belong to you")

        if category and category.user != self.request.user:
            raise PermissionDenied("Category does not belong to you")

        account.balance -= amount
        account.save(update_fields=["balance"])

        serializer.save()


class IncomeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(account__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        account = serializer.validated_data["account"]
        category = serializer.validated_data.get("category")
        amount = serializer.validated_data["amount"]

        if account.user != self.request.user:
            raise PermissionDenied("Account does not belong to you")

        if category and category.user != self.request.user:
            raise PermissionDenied("Category does not belong to you")

        account.balance += amount
        account.save(update_fields=["balance"])

        serializer.save()
