from rest_framework import serializers

from ..models import Inhabitant


class InhabitantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Inhabitant
		fields = ('id', 'username', 'nickname', 'avatar', 'language', 'date_of_birth', 'date_entrance', 'date_leave',
		          'is_superuser')

	username = serializers.CharField(source='user.username')
	is_superuser = serializers.BooleanField(source='user.is_superuser')
