from django.db import models

from .Expense import Expense
from .Inhabitant import Inhabitant


class Debitor(models.Model):
	class Meta:
		unique_together = [['inhabitant', 'expense']]

	inhabitant = models.ForeignKey(Inhabitant, on_delete=models.PROTECT)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
	amount = models.IntegerField()
