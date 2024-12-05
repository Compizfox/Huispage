from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Inhabitant

@api_view(['GET'])
def get_balance(_) -> Response:
	inhabitants = Inhabitant.objects.raw("""
		WITH debitor_balances AS (
		    -- Calculate the total balance adjustment for debitors
		    SELECT i.id, SUM((e.total_amount / debitor_total.total_debitor_amount) * d.amount) AS debitor_balance
		    FROM src_debitor d
		    JOIN src_expense e ON d.expense_id = e.id
		    JOIN src_inhabitant i ON d.inhabitant_id = i.id
		    JOIN (
		        -- Subquery to calculate the total debitor.amount per expense
		        SELECT expense_id, SUM(amount) AS total_debitor_amount
		        FROM src_debitor
		        GROUP BY expense_id
		    ) debitor_total ON e.id = debitor_total.expense_id
		    GROUP BY i.id
		),
		creditor_balances AS (
		    -- Calculate the total balance adjustment for creditors
		    SELECT i.id,
		           SUM(e.total_amount) AS creditor_balance
		    FROM src_expense e
		    JOIN src_inhabitant i ON e.creditor_id = i.id
		    GROUP BY i.id
		)
		-- Combine the starting balance with the calculated debitor and creditor balances
		SELECT i.id,
		       i.start_balance
		       - COALESCE(db.debitor_balance, 0)  -- Add debitor balance changes (if any)
		       + COALESCE(cb.creditor_balance, 0) AS total_balance  -- Add creditor balance changes (if any)
		FROM src_inhabitant i
		LEFT JOIN debitor_balances db ON i.id = db.id
		LEFT JOIN creditor_balances cb ON i.id = cb.id;
	""")

	return Response({inhabitant.pk: inhabitant.total_balance for inhabitant in inhabitants})
