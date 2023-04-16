from rest_framework import serializers

from ..models import Meal, Enrolment


class EnrolmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Enrolment
		fields = ('inhabitant', 'note', 'num_guests', 'created_at', 'updated_at')


class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = ('id', 'cook', 'description', 'created_at', 'updated_at', 'date', 'ready_at')
