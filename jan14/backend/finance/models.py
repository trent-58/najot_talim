from django.db import models
from accounts.models import Account, ExpenseCategory, IncomeCategory


class Expense(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)


class Income(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(
        IncomeCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

