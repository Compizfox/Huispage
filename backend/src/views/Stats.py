from django.db import connection
from django.db.models import F
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Inhabitant, Debitor

meal_category: int = 1

inhabitant_ids = Inhabitant.objects.order_by(F('date_leave').desc(nulls_first=True), '-date_entrance').values_list('pk', flat=True)


@api_view(['GET'])
def get_mean_meal_cost(_) -> Response:
	"""
	Get total mean meal cost for each inhabitant
	"""
	with connection.cursor() as cursor:
		cursor.execute("""
			SELECT e.creditor_id as inhabitant_id, AVG(e.total_amount) / AVG(shares) AS avg_meal_cost
			FROM src_expense as e
			JOIN (
			   SELECT SUM(amount) as shares, expense_id
				FROM src_debitor
				GROUP BY expense_id
			) AS b ON e.id = b.expense_id
			WHERE e.category_id = %s
			GROUP BY e.creditor_id
			""", (meal_category,))

		columns = [col[0] for col in cursor.description]
		rows = cursor.fetchall()

	return Response(dict(zip(columns, row)) for row in rows)


@api_view(['GET'])
def get_monthly_meal_cost(_) -> Response:
	"""
	Get monthly meal cost for each inhabitant
	"""
	def get_for_inhabitant(inhabitant_id: int):
		with connection.cursor() as cursor:
			cursor.execute("""
				WITH RECURSIVE months AS (
					SELECT DATE_FORMAT(MIN(date), '%%Y-%%m-01') AS month_start
					FROM src_expense
					UNION ALL
					SELECT DATE_ADD(month_start, INTERVAL 1 MONTH)
					FROM months
					WHERE month_start < DATE_FORMAT(CURRENT_DATE, '%%Y-%%m-01')
				)
				SELECT DATE_FORMAT(m.month_start, '%%Y-%%m') AS yearmonth, AVG(e.total_amount) / AVG(shares) AS cost
				from months m
				LEFT JOIN (src_expense e
					JOIN (
						SELECT SUM(amount) as shares, expense_id
						FROM src_debitor
						GROUP BY expense_id
					) b ON e.id = b.expense_id)
					ON DATE_FORMAT(e.date, '%%Y-%%m') = DATE_FORMAT(m.month_start, '%%Y-%%m')
					AND e.category_id = %s
					AND e.creditor_id = %s
				GROUP BY m.month_start
				ORDER BY m.month_start;
				""", (meal_category, inhabitant_id))

			return cursor.fetchall()

	return Response([(id, get_for_inhabitant(id)) for id in inhabitant_ids])


@api_view(['GET'])
def get_meal_stats(_) -> Response:
	"""
	Get total meal count, enrolment count, and the ratio per inhabitant
	"""
	with connection.cursor() as cursor:
		cursor.execute("""
			SELECT en.inhabitant_id,
			       meal_count,
			       enrolment_count,
			       meal_count / enrolment_count as ratio
			FROM
			    (SELECT creditor_id, COUNT(id) AS meal_count
			     FROM src_expense
			     WHERE category_id = %s
			     AND date > (SELECT MIN(date) FROM src_enrolment WHERE inhabitant_id = creditor_id)
			     GROUP BY creditor_id) e
			JOIN
			    (SELECT inhabitant_id, SUM(n) AS enrolment_count
			     FROM src_enrolment
			     JOIN src_meal
			        ON src_enrolment.date = src_meal.date
			     GROUP BY inhabitant_id) en
			ON e.creditor_id = en.inhabitant_id;
			""", (meal_category,))

		columns = [col[0] for col in cursor.description]
		rows = cursor.fetchall()

	return Response(dict(zip(columns, row)) for row in rows)


@api_view(['GET'])
def get_monthly_meal_stats(_) -> Response:
	"""
	Get monthly meal count, enrolment count, and the ratio per inhabitant
	"""
	def get_for_inhabitant(inhabitant_id: int):
		with connection.cursor() as cursor:
			cursor.execute("""
				WITH RECURSIVE months AS (
				    SELECT DATE_FORMAT(MIN(date), '%%Y-%%m-01') AS month_start
				    FROM src_expense
				    UNION ALL
				    SELECT DATE_ADD(month_start, INTERVAL 1 MONTH)
				    FROM months
				    WHERE month_start < DATE_FORMAT(CURRENT_DATE, '%%Y-%%m-01')
				)
				SELECT ex.yearmonth, meal_count, enrolment_count, meal_count / enrolment_count as ratio
				FROM (
				    SELECT DATE_FORMAT(m.month_start, '%%Y-%%m') AS yearmonth, COUNT(t.id) AS meal_count
				    FROM months m
				    LEFT JOIN src_expense t
				        ON DATE_FORMAT(t.date, '%%Y-%%m') = DATE_FORMAT(m.month_start, '%%Y-%%m')
				        AND t.category_id = %s
				        AND t.creditor_id = %s
				    GROUP BY m.month_start) ex
				JOIN (
				    SELECT DATE_FORMAT(m.month_start, '%%Y-%%m') AS yearmonth,  IFNULL(SUM(t.n), 0) AS enrolment_count
				    FROM months m
				    LEFT JOIN (src_enrolment t
				        JOIN src_meal meal
				            ON meal.date = t.date)
				        ON DATE_FORMAT(t.date, '%%Y-%%m') = DATE_FORMAT(m.month_start, '%%Y-%%m')
				        AND t.inhabitant_id = %s
				    GROUP BY m.month_start) en
				    ON ex.yearmonth = en.yearmonth;
					""", (meal_category, inhabitant_id, inhabitant_id))

			columns = [col[0] for col in cursor.description]
			rows = cursor.fetchall()
			return [dict(zip(columns, row)) for row in rows]

	return Response([(id, get_for_inhabitant(id)) for id in inhabitant_ids])


@api_view(['GET'])
def get_inhabitant_dob_stats(_) -> Response:
	"""
	Get monthly inhabitant age stats
	"""
	with connection.cursor() as cursor:
		cursor.execute("""
			WITH RECURSIVE MonthGenerator AS (
			   SELECT DATE_FORMAT(MIN(date_entrance), '%Y-%m-01') AS month
			   FROM src_inhabitant
			   UNION ALL
			   SELECT DATE_ADD(month, INTERVAL 1 MONTH)
			   FROM MonthGenerator
			   WHERE month < (SELECT MAX(COALESCE(DATE_FORMAT(date_leave, '%Y-%m-01'), DATE_FORMAT(CURDATE(), '%Y-%m-01'))) FROM src_inhabitant)
			)
			SELECT
			   DATE_FORMAT(mg.month, '%Y-%m') AS yearmonth,
			   AVG(TIMESTAMPDIFF(DAY, p.date_of_birth, mg.month) / 365.25) AS avg_age,
			   MIN(TIMESTAMPDIFF(DAY, p.date_of_birth, mg.month) / 365.25) AS min_age,
			   MAX(TIMESTAMPDIFF(DAY, p.date_of_birth, mg.month) / 365.25) AS max_age
			FROM
			   MonthGenerator mg
			JOIN src_inhabitant p
			   ON mg.month BETWEEN DATE_FORMAT(p.date_entrance, '%Y-%m-01') AND COALESCE(DATE_FORMAT(p.date_leave, '%Y-%m-01'), mg.month)
			GROUP BY mg.month
			ORDER BY mg.month;
			""")
		columns = [col[0] for col in cursor.description]
		rows = cursor.fetchall()

	return Response(dict(zip(columns, row)) for row in rows)
