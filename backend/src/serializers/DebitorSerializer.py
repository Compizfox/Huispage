from rest_framework import serializers

from ..models import Debitor


class DebitorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Debitor
		fields = ('inhabitant', 'amount')
