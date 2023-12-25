export interface Expense {
	creditor_id?: number,
	creditor_name?: string,
	date: string,
	updated_at?: string,
	created_at?: string,
	description: string,
	category?: number,
	total_amount: number,
	unit_price?: number,
	debitors: Array<{
		inhabitant: number,
		amount: number,
	}>
}
