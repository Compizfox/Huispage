from django.db import models

from .Expense import Expense


class ExpenseItem(models.Model):
	name = models.CharField(max_length=25)
	cost = models.DecimalField(max_digits=5, decimal_places=2)
	expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='items')
