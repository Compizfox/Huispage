export interface Expense {
	creditor_id: number | null,
	date: string,
	updated_at: string,
	created_at: string,
	description: string,
	category: number | null,
	total_amount: number | null,
	unit_price: number | null,
	debitors: Array<{
		inhabitant: number,
		amount: number,
	}>
}
