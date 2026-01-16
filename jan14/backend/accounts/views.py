from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Account, ExpenseCategory, IncomeCategory
from .serializers import (
    AccountSerializer,
    ExpenseCategorySerializer,
    IncomeCategorySerializer,
)


class UserOwnedQuerysetMixin:
    permission_classes = [IsAuthenticated]
    model = None
    request = None

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AccountListCreateView(UserOwnedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    model = Account


class AccountRetrieveUpdateDestroyView(UserOwnedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    model = Account


class ExpenseCategoryListCreateView(UserOwnedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = ExpenseCategorySerializer
    model = ExpenseCategory


class ExpenseCategoryRetrieveUpdateDestroyView(UserOwnedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseCategorySerializer
    model = ExpenseCategory


class IncomeCategoryListCreateView(UserOwnedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = IncomeCategorySerializer
    model = IncomeCategory


class IncomeCategoryRetrieveUpdateDestroyView(UserOwnedQuerysetMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeCategorySerializer
    model = IncomeCategory
