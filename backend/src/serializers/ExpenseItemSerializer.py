from rest_framework import serializers

from ..models import ExpenseItem


class ExpenseItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExpenseItem
		fields = ('name', 'cost')
