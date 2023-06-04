import csv
from io import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser

from ..models import Expense, Inhabitant, Debitor, ExpenseCategory


class ExpenseImportSerializer(serializers.Serializer):
	file = serializers.FileField()
	debitor_mapping = serializers.JSONField()
	expense_category_mapping = serializers.JSONField()

	def save(self):
		print(self.validated_data)
		file: InMemoryUploadedFile = self.validated_data['file']
		debitor_map = self.validated_data['debitor_mapping']
		expense_category_map = self.validated_data['expense_category_mapping']

		# This ordeal with .read().decode() through StringIO is a really roundabout way but stupid Django File does
		# not support opening in text mode
		for row in csv.DictReader(StringIO(file.read().decode(encoding=file.charset or 'utf-8')), delimiter='\t'):
			created = False
			try:
				creditor = Inhabitant.objects.get(nickname=row['Betaler'].split()[0])

				(expense, created) = Expense.objects.update_or_create(
					creditor=creditor,
					description=row['Omschrijving'],
					defaults={
						'creditor'    : creditor,
						'category'    : ExpenseCategory.objects.get(name=expense_category_map[row['Soort']]),
						'total_amount': row['Prijs'],
						'description' : row['Omschrijving'],
						'date'        : row['Datum']
					}
				)
				if not created:
					continue

				# Loop over debitors
				for k, v in row.items():
					if k in ('k1', 'k2', 'k3', 'k4', 'k5') and int(v) != 0:
						Debitor.objects.create(
							inhabitant=Inhabitant.objects.get(nickname=debitor_map[k]),
							expense=expense,
							amount=v
						)
			except:
				if created:
					expense.delete()


class ExpenseImportView(CreateAPIView):
	parser_classes = (MultiPartParser,)
	permission_classes = [IsAdminUser]
	serializer_class = ExpenseImportSerializer
