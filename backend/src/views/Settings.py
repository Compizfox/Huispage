from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from django.conf import settings


@api_view(['GET'])
def get_settings(request: Request) -> Response:
	return Response({
		'publicly_editable_debitors': settings.HUISPAGE_PUBLICLY_EDITABLE_DEBITORS,
	})
