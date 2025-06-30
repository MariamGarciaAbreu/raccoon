from django.contrib import admin
from .models import Transaction, TransactionCategory

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'date', 'category')
    search_fields = ('description', 'category__name')
    list_filter = ('date', 'category')

@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('label',)
    search_fields = ('label',)