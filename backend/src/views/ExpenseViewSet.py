from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from django.conf import settings

from ..models import Expense
from ..serializers import ExpenseSerializer


class Pagination(PageNumberPagination):
	page_size = 25
	page_size_query_param = 'page_size'

	# Interpret sentinel value of page_size=0 as all
	def paginate_queryset(self, queryset, request, view=None):
		self.max_page_size = queryset.count()
		return super().paginate_queryset(queryset, request, view=None)

	def get_page_size(self, request):
		if self.page_size_query_param:
			ret = int(request.query_params[self.page_size_query_param])
			if ret < 0:
				return self.page_size
			elif ret == 0:
				return self.max_page_size
			else:
				return ret


class ExpenseViewSet(viewsets.ModelViewSet):
	queryset = Expense.objects
	serializer_class = ExpenseSerializer
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['category', 'creditor', 'debitors']
	ordering = ['-date', '-updated_at']
	pagination_class = Pagination

	def update(self, request: Request, *args, **kwargs) -> Response:
		if not kwargs.get('partial'):
			# Deny updating others' expenses for non-admin users
			if request.data['creditor_id'] != request.user.inhabitant.pk and not \
			   request.user.is_superuser and not \
			   settings.HUISPAGE_PUBLICLY_EDITABLE_DEBITORS:
				raise PermissionDenied

		return super().update(request, *args, **kwargs)

	def partial_update(self, request: Request, *args, **kwargs) -> Response:
		# Only allow updating own debitor amount
		for k, v in request.data.items():
			if k != 'debitors':
				raise PermissionDenied
			else:
				for debitor in v:
					if debitor['inhabitant'] != request.user.inhabitant.pk:
						raise PermissionDenied

		return super().partial_update(request, *args, **kwargs)
