from rest_framework import serializers

from ..models import Inhabitant


class DebitorSerializer(serializers.ModelSerializer):
	inhabitant = serializers.IntegerField(source='id')
	amount = serializers.IntegerField()

	class Meta:
		model = Inhabitant
		fields = ('inhabitant', 'amount')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		if not data['amount']:
			data['amount'] = 0
		return data
