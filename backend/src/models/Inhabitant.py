import datetime
from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Inhabitant(models.Model):
	def default_enrolment_preference() -> dict[int, int]:
		return {
			0: 1,
			1: 1,
			2: 1,
			3: 1,
			4: 1,
			5: 0,
			6: 0,
		}

	user = models.OneToOneField(User, on_delete=models.CASCADE)

	nickname = models.CharField(max_length=25)
	enrolment_preference = models.JSONField(default=default_enrolment_preference)
	avatar = models.ImageField(blank=True)
	language = models.CharField(max_length=2)
	start_balance = models.DecimalField(max_digits=5, decimal_places=2)

	date_of_birth = models.DateField()
	date_entrance = models.DateField()
	date_leave = models.DateField(blank=True, null=True)

	def is_active(self) -> bool:
		"""
		Return true if currently inhabiting.
		"""
		return self.date_leave is None and self.date_entrance < timezone.now()

	def __str__(self) -> str:
		return self.user.__str__()

	def save(self, *args, **kwargs):
		if not self.nickname:
			self.nickname = self.user.first_name

		super().save()

	def get_enrolment_preference(self, date: datetime.date) -> int:
		# JSON field is indexed by strings
		return self.enrolment_preference[str(date.weekday())]

	def get_enrolment_or_preference(self, date: datetime.date) -> int:
		enrolment = self.enrolments.filter(date=date).first()
		return enrolment.n if enrolment else self.get_enrolment_preference(date)

	def get_balance(self) -> Decimal:
		return sum([-debitor.expense.unit_price * debitor.amount for debitor in self.debitor_set.all()] +
		           [expense.total_amount for expense in self.paid_expenses.all()]) + self.start_balance
