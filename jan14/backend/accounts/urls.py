from django.urls import path
from .views import (
    AccountListCreateView,
    AccountRetrieveUpdateDestroyView,
    ExpenseCategoryListCreateView,
    ExpenseCategoryRetrieveUpdateDestroyView,
    IncomeCategoryListCreateView,
    IncomeCategoryRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("accounts/", AccountListCreateView.as_view(), name="list-create"),
    path(
        "accounts/<int:pk>/",
        AccountRetrieveUpdateDestroyView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "expense-categories/",
        ExpenseCategoryListCreateView.as_view(),
        name="expense-list-create",
    ),
    path(
        "expense-categories/<int:pk>/",
        ExpenseCategoryRetrieveUpdateDestroyView.as_view(),
        name="expense-retrieve-update-destroy",
    ),
    path(
        "income-categories/",
        IncomeCategoryListCreateView.as_view(),
        name="income-list-create",
    ),
    path(
        "income-categories/<int:pk>/",
        IncomeCategoryRetrieveUpdateDestroyView.as_view(),
        name="income-retrieve-update-destroy",
    ),
]
