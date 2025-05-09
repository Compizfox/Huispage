from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.permissions import AllowAny

from ..serializers import InhabitantSerializer


@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def set_csrf_token(request: Request) -> Response:
	"""
	Set a CSRF cookie.
	"""
	return Response({})


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request: Request) -> Response:
	"""

	:param request:
	:return:
	"""
	username = request.data.get('username')
	password = request.data.get('password')

	if username is None or password is None:
		raise AuthenticationFailed(detail='Missing username and/or password')

	user = authenticate(username=username, password=password)

	if user is None:
		raise AuthenticationFailed('invalid_credentials')

	if not user.inhabitant.is_active() and not user.is_superuser:
		raise PermissionDenied('inactive')

	auth_login(request, user)

	# Return Inhabitant
	return Response(InhabitantSerializer(user.inhabitant).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def logout(request: Request) -> Response:
	if not request.user.is_authenticated:
		raise AuthenticationFailed(detail='Not logged in')

	auth_logout(request)
	return Response({'detail': 'Success'})
