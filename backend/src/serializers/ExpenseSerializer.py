from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models import Expense, Inhabitant, Debitor, ExpenseItem
from .DebitorSerializer import DebitorSerializer
from .ExpenseItemSerializer import ExpenseItemSerializer


class ExpenseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Expense
		fields = ('id', 'creditor_id', 'creditor_name', 'debitors', 'category', 'date', 'created_at', 'updated_at',
		          'total_amount', 'unit_price', 'description')

	debitors = DebitorSerializer(source='get_debitors', many=True)
	creditor_id = serializers.PrimaryKeyRelatedField(source='creditor', queryset=Inhabitant.objects.all())
	creditor_name = serializers.StringRelatedField(source='creditor')

	def create(self, validated_data: dict) -> Expense:
		# Handle creation for relation: create debitors
		debitors_data = validated_data.pop('get_debitors')
		expense = Expense.objects.create(**validated_data)

		for debitor_data in debitors_data:
			if debitor_data['amount'] != 0:
				Debitor.objects.create(expense=expense, **debitor_data)
		return expense

	def update(self, instance: Expense, validated_data: dict) -> Expense:
		# Handle updating for relation: create/update/delete debitors
		for debitor_data in validated_data.pop('get_debitors'):
			try:
				if debitor_data['amount']:
					debitor = Debitor.objects.get(expense=instance, inhabitant=debitor_data['inhabitant'])
					for key, value in debitor_data.items():
						setattr(debitor, key, value)
					debitor.save()
				else:
					Debitor.objects.filter(expense=instance, inhabitant=debitor_data['inhabitant']).delete()
			except Debitor.DoesNotExist:
				Debitor.objects.create(expense=instance, **debitor_data)

		for attr, value in validated_data.items():
			setattr(instance, attr, value)

		instance.save()
		return instance

	def validate(self, data):
		"""
		Assert that sum of debitor shares is not negative.
		"""
		total_amount = sum([item['amount'] for item in data['get_debitors']])
		if total_amount < 0:
			raise serializers.ValidationError('Sum of debitor shares should be > 0')

		return data


class ExpenseSerializerWithItems(ExpenseSerializer):
	class Meta:
		model = Expense
		fields = ('id', 'creditor_id', 'creditor_name', 'debitors', 'category', 'date', 'created_at', 'updated_at',
		          'total_amount', 'unit_price', 'description', 'items')

	items = ExpenseItemSerializer(many=True)

	def to_internal_value(self, data) -> dict:
		# Omit fully empty expense items
		data['items'] = [item for item in data['items'] if not all(not x for x in item.values())]

		return super().to_internal_value(data)

	def create(self, validated_data: dict) -> Expense:
		items_data = validated_data.pop('items')
		expense = super().create(validated_data)

		# Create items
		for item_data in items_data:
			ExpenseItem.objects.create(expense=expense, **item_data)

		return expense

	def update(self, instance: Expense, validated_data: dict) -> Expense:
		# Update items
		for old_item in instance.items.all():
			old_item.delete()
		for item_data in validated_data.pop('items'):
			ExpenseItem.objects.create(expense=instance, **item_data)

		return super().update(instance, validated_data)
