from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination

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
	queryset = Expense.objects.prefetch_related('debitor_set')
	serializer_class = ExpenseSerializer
	filter_backends = [DjangoFilterBackend, OrderingFilter]
	filterset_fields = ['category', 'creditor', 'debitors']
	ordering = ['-date']
	pagination_class = Pagination

	def update(self, request: Request, *args, **kwargs) -> Response:
		# Deny updating others' expenses for non-admin users

		if request.data['creditor_id'] != request.user.inhabitant.pk and not request.user.is_superuser:
			raise PermissionDenied

		return super().update(request, *args, **kwargs)
