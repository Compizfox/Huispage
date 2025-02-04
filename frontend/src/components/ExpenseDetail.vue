<template>
	<NestedCardDialog ref="dialog">
		<template #title>
			<q-icon name="receipt_long"/>
			{{ expense.description }}
		</template>
		<ExpenseForm
			ref="form"
			v-model="expense"
			@onSubmit="onSubmit"
			:readOnly="readOnly"
			:publiclyEditableAmount="settingsStore.server.publicly_editable_debitors"
		/>
		<q-card-actions align="around">
			<q-btn
				flat
				rounded
				icon="delete"
				:label="t('to_delete')"
				color="negative"
				@click="onDelete"
				v-close-popup
			/>
			<q-btn
				flat
				rounded
				icon="save"
				:label="t('to_save')"
				@click="onSubmit"
				color="primary"
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {computed, Ref, ref} from 'vue'
import ExpenseForm from 'components/ExpenseForm.vue'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import {useAuthStore} from 'stores/auth'
import {useRoute} from 'vue-router'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useSettingsStore} from 'stores/settings'
import type {Expense} from 'src/models/Expense'
import {useI18n} from 'vue-i18n'
import axios from 'axios'
import {useQuasar} from 'quasar'

const {t} = useI18n()
const route = useRoute()
const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const settingsStore = useSettingsStore()
const $q = useQuasar()

const expense: Ref<Expense> = ref({} as Expense)
const url = 'expenses/' + route.params.id + '/'

const form = ref()
const dialog = ref()

fetch()

const readOnly = computed(() =>
	expense.value.creditor_id != authStore.inhabitant?.id &&
	!(authStore.inhabitant?.is_superuser && settingsStore.adminMode)
)

async function fetch() {
	const response = await authStore.request({
		url: url,
		method: 'get',
	})

	expense.value = response?.data

	if (!settingsStore.showAllInhabitants) {
		// Filter out non-current inhabitants that are not debitors
		expense.value.debitors = expense.value.debitors.filter(debitor =>
			inhabitantsStore.getCurrentInhabitants.some(inhabitant => inhabitant.id === debitor.inhabitant) ||
			debitor.amount !== 0)
	}
}

async function onSubmit() {
	const valid = await form.value.validate()
	if (!valid) return

	if (readOnly.value && settingsStore.server.publicly_editable_debitors) {
		// Perform partial update
		await authStore.request({
			url: url,
			method: 'patch',
			data: {
				debitors: [{
					inhabitant: authStore.inhabitant!.id,
					amount: expense.value.debitors.find(x => x.inhabitant === authStore.inhabitant!.id)?.amount,
				}]
			}
		})

		dialog.value.hide()
	} else {
		try {
			await authStore.request({
				url: url,
				method: 'put',
				data: expense.value,
			})

			dialog.value.hide()
		} catch (e) {
			if (axios.isAxiosError(e) && 'non_field_errors' in e.response?.data) {
				$q.notify({
					type: 'negative',
					message: t('double_meal_expense'),
				})
				return
			}
			throw e
		}
	}
}

async function onDelete() {
	await authStore.request({
		url: url,
		method: 'delete',
	})

	dialog.value.hide()
}
</script>
