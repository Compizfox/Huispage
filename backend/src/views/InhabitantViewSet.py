from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import serializers

from ..models import Inhabitant


class InhabitantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Inhabitant
		fields = ('id', 'username', 'email', 'first_name', 'last_name', 'nickname', 'language', 'start_balance',
		          'enrolment_preference', 'date_of_birth', 'date_entrance', 'date_leave', 'is_superuser')
		extra_kwargs = {'password': {'write_only': True}}

	username = serializers.CharField(source='user.username')
	email = serializers.CharField(source='user.email')
	first_name = serializers.CharField(source='user.first_name')
	last_name = serializers.CharField(source='user.last_name')
	is_superuser = serializers.BooleanField(source='user.is_superuser')

	def to_internal_value(self, data: dict) -> dict:
		# Convert empty string to None
		if not data['date_leave']:
			data['date_leave'] = None
		return super().to_internal_value(data)

	def create(self, validated_data: dict) -> Inhabitant:
		# Create User object first
		user_data = validated_data.pop('user')
		user = User.objects.create_user(
			user_data.get('username'),
			user_data.get('email'),
			user_data.get('password')
		)
		user.first_name = user_data.get('first_name')
		user.last_name = user_data.get('last_name')
		user.is_superuser = user_data.get('is_superuser')
		user.save()

		return Inhabitant.objects.create(user=user, **validated_data)

	def update(self, instance: Inhabitant, validated_data: dict) -> Inhabitant:
		# Update User object
		user_data = validated_data.pop('user')
		password = user_data.pop('password', None)
		if password:
			instance.user.set_password(password)

		for key, value in user_data.items():
			setattr(instance.user, key, value)

		instance.user.save()

		for key, value in validated_data.items():
			setattr(instance, key, value)

		instance.save()
		return instance


class InhabitantViewSet(viewsets.ModelViewSet):
	queryset = Inhabitant.objects.all()
	serializer_class = InhabitantSerializer

	def get_queryset(self):
		# Only allow access to own Inhabitant object if not admin
		if self.request.user.is_superuser:
			return Inhabitant.objects.all()
		else:
			return Inhabitant.objects.filter(user=self.request.user)

	def create(self, request: Request, *args, **kwargs) -> Response:
		# Deny creating Inhabitant for non-admin users
		if not request.user.is_superuser:
			raise PermissionDenied

		return super().create(request, *args, **kwargs)
