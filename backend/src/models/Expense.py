from django.db import models
from django.apps import apps

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

	def get_debitors(self):
		"""
		Get a list of Debitors for each Inhabitant, including those for which a Debitor entry does not exist (i.e.
		outer join)
		"""
		Debitor = apps.get_model('src', 'Debitor')

		debitors = []
		for inhabitant in Inhabitant.objects.prefetch_related('debitor_set__expense').all():
			try:
				debitors.append(inhabitant.debitor_set.get(expense=self))
			except Debitor.DoesNotExist:
				debitors.append(Debitor(inhabitant=inhabitant, amount=None))

		return debitors
