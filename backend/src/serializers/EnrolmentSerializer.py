from rest_framework import serializers

from ..models import Enrolment


class EnrolmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Enrolment
		fields = ('inhabitant', 'date', 'note', 'n', 'created_at', 'updated_at')
