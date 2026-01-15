from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Account, ExpenseCategory, IncomeCategory
from .serializers import (
    AccountSerializer,
    ExpenseCategorySerializer,
    IncomeCategorySerializer,
)


class UserOwnedQuerysetMixin:
    """Ensure objects are always scoped to request.user and user is set on create."""

    permission_classes = [IsAuthenticated]
    model = None  # set in subclasses

    # Populated by DRF GenericAPIView at runtime; declared here for type checkers/IDEs.
    request = None

    def get_queryset(self):
        # Works for list + retrieve/update/destroy by limiting lookup to the user-owned subset.
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
