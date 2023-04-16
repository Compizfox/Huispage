from rest_framework import serializers

from ..models import Enrolment


class EnrolmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Enrolment
		fields = ('inhabitant', 'date', 'note', 'num_guests', 'value', 'created_at', 'updated_at')
