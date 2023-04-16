export interface Expense {
	creditor_id: number,
	date: string,
	description: string,
	category: number | null,
	total_amount: number | null,
	debitors: Array<{
		inhabitant: number,
		amount: number,
	}>
}
