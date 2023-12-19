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
import {date} from 'quasar'
import {computed, ref, Ref} from 'vue'
import ExpenseForm from 'components/ExpenseForm.vue'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import {useAuthStore} from 'stores/auth';
import {useInhabitantsStore} from 'stores/inhabitants'
import {useI18n} from 'vue-i18n'

import type {Expense} from 'src/models/Expense'
import {useSettingsStore} from 'stores/settings'

const {t} = useI18n()
const $q = useQuasar()
const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore();
const settingsStore = useSettingsStore();

const url = 'expenses/'

// New empty Expense
const expense: Ref<Expense> = ref({
	creditor_id: authStore.inhabitant!.id,
	date: date.formatDate(Date.now(), 'YYYY-MM-DD'),
	description: '',
	category: null,
	total_amount: null,
	debitors: [],
})

const getInhabitants = computed(() =>
	settingsStore.showAllInhabitants ? inhabitantsStore.inhabitants : inhabitantsStore.getCurrentInhabitants
)

// Populate debitors field in expense object with inhabitants and default amounts of 0
inhabitantsStore.fetch().then(() => {
	expense.value.debitors = getInhabitants.value.map((inhabitant) => {
		return {
			inhabitant: inhabitant.id,
			amount: 1,
		}
	})
})

const form = ref()
const dialog = ref()

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
</script>
