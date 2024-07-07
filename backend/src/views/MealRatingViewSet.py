from rest_framework import serializers, viewsets, mixins
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import MealRating


class MealRatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = MealRating
		fields = ('meal', 'rating', 'inhabitant')


class MealRatingViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
	serializer_class = MealRatingSerializer

	def get_queryset(self):
		return MealRating.objects.filter(meal=self.kwargs['meal_pk'], inhabitant=self.request.user)

	def create(self, request: Request, *args, **kwargs) -> Response:
		data = {
			'meal': self.kwargs['meal_pk'],
			'rating': request.data['rating'],
			'inhabitant': request.data['inhabitant']
		}
		try:
			instance = MealRating.objects.get(inhabitant=request.user.inhabitant.pk, meal=self.kwargs['meal_pk'])
			serializer = self.get_serializer(instance, data=data, partial=True)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(serializer.data)
		except MealRating.DoesNotExist:
			serializer = self.get_serializer(data=data)
			serializer.is_valid(raise_exception=True)
			self.perform_create(serializer)
			return Response(serializer.data)
