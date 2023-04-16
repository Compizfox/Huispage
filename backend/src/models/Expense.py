from django.db import models

from .Inhabitant import Inhabitant
from .ExpenseCategory import ExpenseCategory


class Expense(models.Model):
	creditor = models.ForeignKey(Inhabitant, on_delete=models.PROTECT, related_name='paid_expenses')
	debitors = models.ManyToManyField(Inhabitant, through='Debitor', related_name='involved_expenses')
	category = models.ForeignKey(ExpenseCategory, on_delete=models.RESTRICT)

	total_amount = models.DecimalField(max_digits=5, decimal_places=2)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date = models.DateField()

	description = models.CharField(max_length=100, blank=True)

	@property
	def unit_price(self) -> float | None:
		queryset = self.debitor_set.aggregate(models.Sum('amount'))
		if not queryset['amount__sum']:
			return None
		return self.total_amount / queryset['amount__sum']
