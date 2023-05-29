from rest_framework import serializers

from ..models import Debitor


class DebitorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Debitor
		fields = ('inhabitant', 'amount')

	def to_representation(self, instance):
		data = super().to_representation(instance)
		if not data['amount']:
			data['amount'] = 0
		return data
