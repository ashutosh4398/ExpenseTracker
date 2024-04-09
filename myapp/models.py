from django.db import models
from enum import Enum


class Categories(Enum):
    PERSONAL = "PERSONAL"
    BUSINESS = "BUSINESS"

    @classmethod
    def list_choices(self):
        return [(x.name, x.value) for x in self]


# Create your models here.
class Expense(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(
        default=Categories.PERSONAL.value,
        choices=Categories.list_choices(),
        max_length=16,
    )
    amount = models.FloatField()
    date_created = models.DateTimeField(auto_now=True)
