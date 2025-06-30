from django.db.models import fields
from rest_framework import serializers
from .models import Transaction, TransactionCategory

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'description', 'amount', 'date', 'category')

class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ('id', 'name')