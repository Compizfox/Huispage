import {defineStore} from 'pinia'
import {useAuthStore} from 'stores/auth'

export const useExpenseCategoriesStore = defineStore('expenseCategories', {
	state: () => ({
		expenseCategories: [],
	}),

	getters: {
		getExpenseCategories(state) {
			return state.expenseCategories
		}
	},

	actions: {
		async fetch() {
			const response = await useAuthStore().request({url: 'expense_categories/', method: 'get'})
			this.expenseCategories = response?.data
		}
	}
})
