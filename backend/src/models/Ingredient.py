from django.db import models


class Ingredient(models.Model):
	name = models.CharField(max_length=25)
	cost = models.DecimalField(max_digits=5, decimal_places=2)
