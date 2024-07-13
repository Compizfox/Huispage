from datetime import datetime

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied

from ..models import Inhabitant
from ..models import Enrolment
from ..serializers import EnrolmentSerializer


class EnrolmentViewSet(viewsets.ModelViewSet):
	queryset = Enrolment.objects.all()
	serializer_class = EnrolmentSerializer

	def get_queryset(self):
		# Only allow access to own Inhabitant object if not admin
		if self.request.user.is_superuser:
			return Inhabitant.objects.all()
		else:
			return Inhabitant.objects.filter(user=self.request.user)

	def create(self, request: Request, *args, **kwargs) -> Response:
		# Deny creating Enrolments before today for non-admin users
		if datetime.strptime(request.data['date'], "%Y-%m-%d") < datetime.now() and not request.user.is_superuser:
			raise PermissionDenied

		# (Partially) update Enrolment if exists, else create new one
		try:
			instance = Enrolment.objects.get(inhabitant=request.data['inhabitant'], date=request.data['date'])
			serializer = self.get_serializer(instance, data=request.data, partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data)
		except Enrolment.DoesNotExist:
			return super().create(request, *args, **kwargs)
