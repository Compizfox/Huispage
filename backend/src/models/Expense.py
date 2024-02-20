from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from .Inhabitant import Inhabitant
from .ExpenseCategory import ExpenseCategory


class Expense(models.Model):
	creditor = models.ForeignKey(Inhabitant, on_delete=models.PROTECT, related_name='paid_expenses')
	debitors = models.ManyToManyField(Inhabitant, through='Debitor', related_name='involved_expenses')
	category = models.ForeignKey(ExpenseCategory, on_delete=models.RESTRICT)

	total_amount = models.DecimalField(max_digits=5, decimal_places=2, validators=(MinValueValidator(0),))

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date = models.DateField()

	description = models.CharField(max_length=100, blank=True)

	@property
	def unit_price(self) -> Decimal | None:
		"""
		Price per debitor
		"""
		queryset = self.debitor_set.aggregate(models.Sum('amount'))
		if not queryset['amount__sum']:
			return None
		return self.total_amount / queryset['amount__sum']

	def get_debitors(self) -> list:
		"""
		Get a list of Debitors for each Inhabitant, including those for which a Debitor entry does not exist (i.e.
		outer join)
		"""
		query = (
			'SELECT i.id, amount '
			'FROM src_inhabitant as i '
			'LEFT JOIN ( '
			'   SELECT src_debitor.inhabitant_id, src_debitor.amount as amount '
			'   FROM src_debitor '
			'   JOIN src_expense ON src_debitor.expense_id = src_expense.id and src_expense.id = %s) as sol '
			'   ON i.id = sol.inhabitant_id'
		)

		inhabitants = Inhabitant.objects.raw(query, (self.pk,))

		return [{
			'inhabitant': x,
			'amount': x.amount,
		} for x in inhabitants]

	def clean(self):
		if self.debitor_set.aggregate(models.Sum('amount'))['amount__sum'] < 0:
			raise ValidationError('Sum of debitor shares should be > 0')
