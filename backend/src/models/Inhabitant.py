import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Inhabitant(models.Model):
	def default_enrolment_preference() -> dict[int, bool]:
		return {
			0: True,
			1: True,
			2: True,
			3: True,
			4: True,
			5: False,
			6: False,
		}

	user = models.OneToOneField(User, on_delete=models.CASCADE)

	nickname = models.CharField(max_length=25)
	enrolment_preference = models.JSONField(default=default_enrolment_preference)
	avatar = models.ImageField(blank=True)
	language = models.CharField(max_length=2)

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

	def get_enrolment_preference(self, date: datetime.date) -> bool:
		# JSON field is indexed by strings
		return self.enrolment_preference[str(date.weekday())]

	def get_enrolment_or_preference(self, date: datetime.date) -> bool:
		enrolment = self.enrolments.filter(date=date)
		return enrolment[0].value if enrolment.exists() else self.get_enrolment_preference(date)
