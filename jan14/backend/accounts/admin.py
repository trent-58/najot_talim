from django.contrib import admin

from .models import Account, ExpenseCategory, IncomeCategory


class AccountAdmin( admin.ModelAdmin ):
  list_display = [ 'user', 'name', 'type', 'currency', 'balance', 'status', ]
  search_fields = [ 'name', 'user__username', 'currency', ]
  list_filter = [ 'type', 'status', ]
  ordering = ('name',)


class ExpenseCategoryAdmin( admin.ModelAdmin ):
  list_display = [ 'user', 'icon', 'name', ]
  search_fields = [ 'name', 'user__username', ]
  list_filter = [ 'user' ]
  ordering = ('name',)


class IncomeCategoryAdmin( admin.ModelAdmin ):
  list_display = [ 'user', 'name', ]
  search_fields = [ 'name', 'user__username', ]
  list_filter = [ 'user' ]
  ordering = [ 'name' ]


admin.site.register( Account, AccountAdmin )
admin.site.register( ExpenseCategory, ExpenseCategoryAdmin )
admin.site.register( IncomeCategory, IncomeCategoryAdmin )
