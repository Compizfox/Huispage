<template>
	<NestedCardDialog>
		<template #title>
			<q-icon name="receipt_long"/>
			{{ expense.description }}
		</template>
		<ExpenseForm v-model="expense" @onSubmit="onSubmit"/>
		<q-card-actions align="around">
			<q-btn
				flat
				rounded
				icon="delete"
				:label="t('delete')"
				color="negative"
				@click="onDelete"
				v-close-popup
			/>
			<q-btn
				flat
				rounded
				icon="save"
				label="OK"
				@click="onSubmit"
				color="primary"
				v-close-popup
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {onMounted, ref, Ref} from 'vue'
import ExpenseForm from 'components/ExpenseForm.vue'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import {useAuthStore} from 'stores/auth';
import {useRoute} from 'vue-router'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useSettingsStore} from 'stores/settings'

import type {Expense} from 'src/models/Expense'
import {useI18n} from 'vue-i18n'

const {t} = useI18n()
const route = useRoute()
const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore();
const settingsStore = useSettingsStore();

const expense: Ref<Expense> = ref({
	creditor_id: null,
	date: '',
	description: '',
	category: null,
	total_amount: null,
	debitors: [],
})

const url = 'expenses/' + route.params.id + '/'

function fetch() {
	authStore.request({
		url: url,
		method: 'get',
	}).then(response => {
		expense.value = response?.data

		if(!settingsStore.showAllInhabitants) {
			// Filter out non-current inhabitants that are not debitors
			expense.value.debitors = expense.value.debitors.filter(debitor =>
				inhabitantsStore.getCurrentInhabitants.some(inhabitant => inhabitant.id === debitor.inhabitant) ||
				debitor.amount !== 0)
		}
	})
}

function onSubmit() {
	authStore.request({
		url: url,
		method: 'put',
		data: expense.value,
	})
}

function onDelete() {
	authStore.request({
		url: url,
		method: 'delete',
	})
}

onMounted(() => {
	fetch()
})
</script>

<style scoped>

</style>
