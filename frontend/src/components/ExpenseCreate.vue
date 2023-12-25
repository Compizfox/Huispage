<template>
	<NestedCardDialog ref="dialog">
		<template #title>
			<q-icon name="receipt_long"/>
			{{t('new_expense')}}
		</template>
		<ExpenseForm ref="form" v-model="expense" @onSubmit="onSubmit"/>
		<q-card-actions align="right">
			<q-btn
				flat
				rounded
				icon="save"
				label="OK"
				color="primary"
				@click="onSubmit"
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {computed, ref, Ref} from 'vue'
import {date} from 'quasar'
import {useAuthStore} from 'stores/auth';
import {useInhabitantsStore} from 'stores/inhabitants'
import {useI18n} from 'vue-i18n'
import {useRoute} from 'vue-router'
import ExpenseForm from 'components/ExpenseForm.vue'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import type {Expense} from 'src/models/Expense'
import {useSettingsStore} from 'stores/settings'

const {t} = useI18n()
const route = useRoute()
const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore();
const settingsStore = useSettingsStore();

const url = 'expenses/'

// New empty Expense
const expense: Ref<Expense> = ref({
	creditor_id: authStore.inhabitant!.id,
	date: date.formatDate(Date.now(), 'YYYY-MM-DD'),
	description: '',
	category: 1,
	total_amount: 0,
	debitors: [],
})

const getInhabitants = computed(() =>
	settingsStore.showAllInhabitants ? inhabitantsStore.inhabitants : inhabitantsStore.getCurrentInhabitants
)

const form = ref()
const dialog = ref()

// Populate debitors field in expense object with inhabitants and default amounts of 0
inhabitantsStore.fetch().then(() => {
	expense.value.debitors = getInhabitants.value.map((inhabitant) => {
		return {
			inhabitant: inhabitant.id,
			amount: 1,
		}
	})

	if (route.query.meal_id) fetch()
})

async function onSubmit() {
	const valid = await form.value.validate()
	if (!valid) return

	await authStore.request({
		url: url,
		method: 'post',
		data: expense.value,
	})

	dialog.value.hide()
}

async function fetch() {
	// Assign meal data to expense
	{
		const response = await authStore.request({
			url: 'meals/' + route.query.meal_id + '/',
			method: 'get',
		})

		expense.value.category = 1
		expense.value.creditor_id = response?.data.cook
		expense.value.date = response?.data.date
		expense.value.description = response?.data.description
	}

	// Assign the meal enrolments to expense debitors
	{
		const response = await authStore.request({
			url: 'meals/' + route.query.meal_id + '/enrolments/',
			method: 'get',
		})

		expense.value.debitors = expense.value.debitors.map((debitor) => {
			return {
				inhabitant: debitor.inhabitant,
				amount: response?.data.find(x => x.inhabitant === debitor.inhabitant)?.n ?? 0
			}
		})
	}
}
</script>
