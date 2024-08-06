import {Meal} from 'src/models/Meal'

export interface Day {
	date: string,
	meal: Meal,
	enrolments: {
		[key: string]: {
			n: number,
			updated_at: string,
		}
	};
}
