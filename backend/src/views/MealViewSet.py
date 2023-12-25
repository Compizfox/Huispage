from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from ..models import Meal, Enrolment
from ..serializers import MealSerializer


class EnrolmentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Enrolment
		fields = ('inhabitant', 'n')


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

	@action(detail=True)
	def enrolments(self, request, pk):
		enrolments = Enrolment.objects.filter(date=self.get_object().date)
		serializer = EnrolmentSerializer(enrolments, many=True)
		return Response(serializer.data)
