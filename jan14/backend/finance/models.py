from django.db import models
from accounts.models import Account, ExpenseCategory, IncomeCategory

class Expense(models.Model):
    account = models.ForeignKey(Account, related_name='expense', on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, related_name='expense', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Expense {self.id} - {self.amount}"

class Income(models.Model):
    account = models.ForeignKey(Account, related_name='income', on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, related_name='income', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Income {self.id} - {self.amount}"

