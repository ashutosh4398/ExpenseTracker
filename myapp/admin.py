from django.contrib import admin

from .models import Expense

# Register your models here.


@admin.register(Expense)
class ExpenseTable(admin.ModelAdmin):
    list_display = ["id", "name", "amount", "category", "date_created"]
