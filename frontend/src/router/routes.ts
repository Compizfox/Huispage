import {RouteRecordRaw} from 'vue-router';

const routes: RouteRecordRaw[] = [
	{
		path: '/login',
		name: 'login',
		component: () => import('pages/LoginPage.vue'),
	},
	{
		path: '/',
		component: () => import('layouts/MainLayout.vue'),
		children: [
			{
				path: 'meal-planning',
				name: 'mealPlanning',
				component: () => import('pages/MealPlanningPage.vue'),
				children: [
					{
						path: ':id',
						name: 'mealDetail',
						component: () => import('components/MealDetail.vue')
					},
				]
			},
			{
				path: 'expenses',
				name: 'expenses',
				component: () => import('pages/ExpensesPage.vue'),
				children: [
					{
						path: 'create',
						name: 'createExpense',
						component: () => import('components/ExpenseCreate.vue')
					},
					{
						path: ':id',
						name: 'expenseDetail',
						component: () => import('components/ExpenseDetail.vue')
					},
				]
			},
			{
				path: 'fridge-accounting',
				name: 'fridgeAccounting',
				component: () => import('pages/FridgeAccountingPage.vue')
			},
			{
				path: 'stats',
				name: 'stats',
				component: () => import('pages/StatsPage.vue')
			},
			{
				path: 'settings',
				name: 'settings',
				component: () => import('pages/SettingsPage.vue'),
				children: [
					{
						path: 'inhabitants',
						name: 'inhabitants',
						component: () => import('pages/settings/InhabitantsPage.vue')
					}
				]
			},
		],
	},

	// Always leave this as last one,
	// but you can also remove it
	{
		path: '/:catchAll(.*)*',
		component: () => import('pages/ErrorNotFound.vue'),
	},
];

export default routes;
