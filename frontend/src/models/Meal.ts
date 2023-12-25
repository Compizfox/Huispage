export interface Meal {
	id?: number,
	cook: number,
	participants: Array<number>,
	description?: string,
	created_at?: string,
	updated_at?: string,
	date: string,
	ready_at: string,
	expense: number | null,
}
