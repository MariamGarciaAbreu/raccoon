from django.test import TestCase
from models import Transaction, TransactionCategory

TransactionCategory.generate_data(10)  # Generate 10 categories for testing
# Create your tests here.
