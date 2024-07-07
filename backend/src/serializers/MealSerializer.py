from rest_framework import serializers

from .MealRatingSerializer import MealRatingSerializer
from ..models import Meal


class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = ('id', 'cook', 'description', 'created_at', 'updated_at', 'date', 'ready_at', 'expense', 'ratings')

	expense = serializers.IntegerField(source='get_expense', read_only=True)
	ratings = MealRatingSerializer(many=True, read_only=True)
