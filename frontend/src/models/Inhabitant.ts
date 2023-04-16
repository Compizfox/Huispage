export interface Inhabitant {
	id: number,
	username: string,
	nickname: string,
	avatar: string,
	language: string,
	date_of_birth: string,
	date_entrance: string,
	date_leave: string | null,
	is_superuser: boolean,
}
