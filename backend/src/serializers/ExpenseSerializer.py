from rest_framework import serializers

from ..models import Expense, Inhabitant, Debitor
from .DebitorSerializer import DebitorSerializer


class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ('id', 'creditor_id', 'creditor_name', 'debitors', 'category', 'date', 'total_amount', 'unit_price',
		          'description')

	debitors = DebitorSerializer(source='debitor_set', many=True)
	creditor_id = serializers.PrimaryKeyRelatedField(source='creditor', queryset=Inhabitant.objects.all())
	creditor_name = serializers.StringRelatedField(source='creditor')

	def create(self, validated_data: dict) -> Expense:
		# Handle creation for relation: create debitors
		debitors_data = validated_data.pop('debitor_set')
		expense = Expense.objects.create(**validated_data)
		for debitor_data in debitors_data:
			Debitor.objects.create(expense=expense, **debitor_data)
		return expense
