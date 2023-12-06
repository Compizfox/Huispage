from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Inhabitant

@api_view(['GET'])
def get_balance(_) -> Response:
	queryset = Inhabitant.objects.prefetch_related('debitor_set__expense').all()

	return Response({inhabitant.pk: inhabitant.get_balance() for inhabitant in queryset})
