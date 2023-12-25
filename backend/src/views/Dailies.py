import datetime

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import Meal, Inhabitant
from ..serializers import MealSerializer


class DailiesView(APIView):
	"""
	Get daily meals/enrolments for a given week
	"""
	@staticmethod
	def _day(date: datetime.date) -> dict:
		"""
		Fetch and return dict of meal and enrolments for day
		:param date: Date object
		:return: dict of date, meal, and enrolments
		"""
		meal = Meal.objects.filter(date=date).first()

		inhabitants = Inhabitant.objects.filter(date_leave__isnull=True).prefetch_related('enrolments')

		return {
			'date': date,
			'meal': MealSerializer(meal).data if meal else None,
			'enrolments': {inhabitant.pk: inhabitant.get_enrolment_or_preference(date) for inhabitant in inhabitants}
		}

	def get(self, request: Request, year: int, week: int) -> Response:
		firstday = datetime.date.fromisocalendar(year=year, week=week, day=1)

		# Iterate over days in week
		data = [self._day(day) for day in (firstday + datetime.timedelta(days=i) for i in range(7))]

		return Response(data)
