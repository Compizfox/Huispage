import {defineStore} from 'pinia'
import {useAuthStore} from 'stores/auth'
import {Inhabitant} from 'src/models/Inhabitant';

export const useInhabitantsStore = defineStore('inhabitants', {
	state: () => ({
		inhabitants: [] as Array<Inhabitant>,
	}),

	getters: {
		getInhabitants(state) {
			return state.inhabitants
		}
	},

	actions: {
		async fetch() {
			const response = await useAuthStore().request({url: 'inhabitants/', method: 'get'})
			this.inhabitants = response?.data
		}
	}
});
