import datetime
from decimal import Decimal
from typing import Dict

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
		today = timezone.now().date()
		return (self.date_leave is None or today < self.date_leave) and self.date_entrance < today

	def __str__(self) -> str:
		return self.user.__str__()

	def save(self, *args, **kwargs):
		if not self.nickname:
			self.nickname = self.user.first_name

		super().save()

	def get_enrolment_preference(self, date: datetime.date) -> int:
		#                                JSON field is indexed by strings
		return self.enrolment_preference[str(date.weekday())] if self.is_active() else 0

	def get_enrolment_or_preference(self, date: datetime.date) -> Dict:
		enrolment = self.enrolments.filter(date=date).first()
		if enrolment:
			return {
				'n': enrolment.n,
				'updated_at': enrolment.updated_at,
			}
		else:
			return {
				'n': self.get_enrolment_preference(date),
				'updated_at': None,
			}
