from rest_framework import serializers

from ..models import Meal


class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = ('id', 'cook', 'description', 'created_at', 'updated_at', 'date', 'ready_at', 'expense')

	expense = serializers.IntegerField(source='get_expense', read_only=True)
