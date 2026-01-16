from django.urls import path
from .views import  ExpenseListCreateView, IncomeListCreateView

urlpatterns = [
    path("expenses/", ExpenseListCreateView.as_view(), name="expenses"),
    path("incomes/", IncomeListCreateView.as_view(), name="incomes"),

    path("expense/", ExpenseListCreateView.as_view(), name="expense"),
    path("income/", IncomeListCreateView.as_view(), name="income"),
]