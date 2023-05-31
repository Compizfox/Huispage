from django.db import models

from .Inhabitant import Inhabitant


class Enrolment(models.Model):
	class Meta:
		unique_together = [['date', 'inhabitant']]
		ordering = ['created_at']

	inhabitant = models.ForeignKey(Inhabitant, on_delete=models.CASCADE, related_name='enrolments')
	date = models.DateField()
	note = models.CharField(max_length=100, blank=True)
	n = models.PositiveIntegerField(default=1)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return self.inhabitant.user.username + ' ' + self.date.__str__()
