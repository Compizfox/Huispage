from rest_framework import viewsets

from ..models import Inhabitant
from ..serializers import InhabitantSerializer


class InhabitantViewSet(viewsets.ModelViewSet):
	queryset = Inhabitant.objects.filter(date_leave__isnull=True)
	serializer_class = InhabitantSerializer
