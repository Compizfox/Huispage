from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Meal
from ..serializers import MealSerializer


class MealViewSet(viewsets.ModelViewSet):
	queryset = Meal.objects.all()
	serializer_class = MealSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['date']

	def create(self, request: Request, *args, **kwargs) -> Response:
		# Deny creating Meal for others for non-admin users
		if request.data['cook'] != request.user.inhabitant.pk and not request.user.is_superuser:
			raise PermissionDenied

		return super().create(request, *args, **kwargs)

	def update(self, request: Request, *args, **kwargs) -> Response:
		# Deny updating Meal for others for non-admin users
		if request.data['cook'] != request.user.inhabitant.pk and not request.user.is_superuser:
			raise PermissionDenied

		return super().update(request, *args, **kwargs)
