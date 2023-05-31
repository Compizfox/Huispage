<template>
	<NestedCardDialog>
		<template #title>
			<q-icon name="receipt_long"/>
			New expense
		</template>
		<ExpenseForm v-model="expense" @onSubmit="onSubmit"/>
		<q-card-actions align="right">
			<q-btn
				flat
				rounded
				icon="save"
				label="OK"
				color="primary"
				@click="onSubmit"
				v-close-popup
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {ref, Ref} from 'vue';
import type {Expense} from 'src/models/Expense'
import {date} from 'quasar';
import ExpenseForm from 'components/ExpenseForm.vue';
import NestedCardDialog from 'components/NestedCardDialog.vue';
import {useAuthStore} from 'stores/auth';
import {useInhabitantsStore} from 'stores/inhabitants'

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore();

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

// Populate debitors field in expense object with inhabitants and default amounts of 0
inhabitantsStore.fetch().then(() => {
	expense.value.debitors = inhabitantsStore.getCurrentInhabitants.map((inhabitant) => {
		return {
			inhabitant: inhabitant.id,
			amount: 0,
		}
	})
})

function onSubmit() {
	authStore.request({
		url: url,
		method: 'post',
		data: expense.value,
	})
}
</script>

<style scoped>

</style>
