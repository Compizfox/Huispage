from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from ..models import Expense
from ..serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
	queryset = Expense.objects.all()
	serializer_class = ExpenseSerializer
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['category', 'creditor', 'debitors']
