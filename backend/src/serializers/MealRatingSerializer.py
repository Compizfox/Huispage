from rest_framework import serializers

from ..models import MealRating


class MealRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = MealRating
		fields = ('rating',)


