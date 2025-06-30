from django.db import models

class Transaction(models.Model):

    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('TransactionCategory', on_delete=models.CASCADE)

    def __str__(self):
        return self.description

class TransactionCategory(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # @classmethod
    # def generate_data(cls, count=10):
    #     from mimesis import Person
    #     from mimesis.locales import Locale
    #     from mimesis import Generic
    #     generic = Generic(Locale.EN)
    #     for _ in range(count):
    #         cls.objects.create(name=generic.text.word())