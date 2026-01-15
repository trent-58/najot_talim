from django.urls import path

from .views import ExpenseDetailView, ExpenseListCreateView, IncomeDetailView, IncomeListCreateView

urlpatterns = [
    # Frontend-expected (plural)
    path("expenses/", ExpenseListCreateView.as_view(), name="expenses"),
    path("expenses/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail"),
    path("incomes/", IncomeListCreateView.as_view(), name="incomes"),
    path("incomes/<int:pk>/", IncomeDetailView.as_view(), name="income-detail"),

    # Backwards-compatible (previous singular)
    path("expense/", ExpenseListCreateView.as_view(), name="expense"),
    path("expense/<int:pk>/", ExpenseDetailView.as_view(), name="expense-detail-old"),
    path("income/", IncomeListCreateView.as_view(), name="income"),
    path("income/<int:pk>/", IncomeDetailView.as_view(), name="income-detail-old"),
]
