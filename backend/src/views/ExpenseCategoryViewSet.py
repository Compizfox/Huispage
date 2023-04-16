from rest_framework import viewsets

from ..models import ExpenseCategory
from ..serializers import ExpenseCategorySerializer


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
	queryset = ExpenseCategory.objects.all()
	serializer_class = ExpenseCategorySerializer
