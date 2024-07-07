from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .Meal import Meal
from .Inhabitant import Inhabitant


class MealRating(models.Model):
	class Meta:
		unique_together = [['meal', 'inhabitant']]

	meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ratings')
	inhabitant = models.ForeignKey(Inhabitant, on_delete=models.CASCADE, related_name='ratings')

	rating = models.IntegerField(validators=(MinValueValidator(1), MaxValueValidator(5)))

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
