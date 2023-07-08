from rest_framework import generics
from django.db.models import F

from ..models import Inhabitant
from ..serializers import InhabitantSerializer


class InhabitantList(generics.ListAPIView):
	queryset = Inhabitant.objects.all().order_by(F('date_leave').desc(nulls_first=True))
	serializer_class = InhabitantSerializer
