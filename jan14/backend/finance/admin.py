from django.contrib import admin
from .models import Expense, Income


class ExpenseAdmin(admin.ModelAdmin):
  list_display = ['account', 'category', 'amount', 'note']
  list_filter = ['account', 'category']
  search_fields = ['amount', 'note']
  ordering = ['-created_at']



class IncomeAdmin(admin.ModelAdmin):
  list_display = ['account', 'category', 'amount', 'note']
  list_filter = ['account', 'category']
  search_fields = ['amount', 'note']
  ordering = ['-created_at']


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)