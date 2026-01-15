from django.db import models
from users.models import User

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('CURRENCY', 'Currency'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]

    user = models.ForeignKey(User, related_name='accounts',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    type = models.CharField(
        max_length=10,
        choices=ACCOUNT_TYPE_CHOICES,
        default='CASH',
    )
    currency = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE',
    )

    def __str__(self):
        return f"{self.name} ({self.type}) - {self.currency} {self.balance}"


class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, related_name="expense_categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class IncomeCategory(models.Model):
    user = models.ForeignKey(User, related_name="income_categories",on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name