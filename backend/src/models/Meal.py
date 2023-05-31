from django.db import models

from .Expense import Expense
from .Inhabitant import Inhabitant
from .Enrolment import Enrolment


class Meal(models.Model):
	class Meta:
		ordering = ['created_at']

	cook = models.ForeignKey(Inhabitant, on_delete=models.CASCADE, related_name='cooked_meals')
	expense = models.OneToOneField(Expense, on_delete=models.SET_NULL, null=True, blank=True, default=None)

	description = models.CharField(max_length=25, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	date = models.DateField(unique=True)
	ready_at = models.TimeField()

	@property
	def enrolments(self):
		return Enrolment.objects.filter(date=self.date)

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		# Make enrolment preferences explicit for this date
		for inhabitant in Inhabitant.objects.filter(date_leave__isnull=True):
			Enrolment.objects.get_or_create(inhabitant=inhabitant, date=self.date,
			                                defaults={'n': inhabitant.get_enrolment_preference(self.date)})
