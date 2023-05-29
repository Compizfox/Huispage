from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied

from ..models import Expense
from ..serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
	queryset = Expense.objects.all()
	serializer_class = ExpenseSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['category', 'creditor', 'debitors']

	def update(self, request: Request, *args, **kwargs) -> Response:
		# Deny updating others' expenses for non-admin users

		if request.data['creditor_id'] != request.user.inhabitant.pk and not request.user.is_superuser:
			raise PermissionDenied

		return super().update(request, *args, **kwargs)
