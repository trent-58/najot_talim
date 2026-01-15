from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Expense, Income
from .serializers import ExpenseSerializer, IncomeSerializer


class ExpenseListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data.get("account")
        if account.user_id != self.request.user.id:
            raise PermissionDenied("Account does not belong to you")
        serializer.save()


class IncomeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data.get("account")
        if account.user_id != self.request.user.id:
            raise PermissionDenied("Account does not belong to you")
        serializer.save()


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(account__user=self.request.user)


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(account__user=self.request.user)
