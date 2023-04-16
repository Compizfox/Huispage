<template>
	<q-form class="q-gutter-md">
		<q-select
			emit-value
			map-options
			:options="expenseCategoriesStore.getExpenseCategories"
			option-value="id"
			option-label="name"
			v-model="expenseModel.category"
			label="Categorie"
		>
			<template v-slot:option="scope">
				<q-item v-bind="scope.itemProps">
					<q-item-section avatar>
						<q-icon :name="scope.opt.icon"/>
					</q-item-section>
					<q-item-section>
						<q-item-label>{{ scope.opt.name }}</q-item-label>
					</q-item-section>
				</q-item>
			</template>
		</q-select>

		<q-input
			filled
			v-model="expenseModel.description"
			label="Omschrijving"
		/>

		<q-input
			filled
			v-model="expenseModel.date"
			mask="date"
			:rules="['date']"
			hide-bottom-space
		>
			<template v-slot:append>
				<q-icon name="event" class="cursor-pointer">
					<q-popup-proxy ref="datepickerProxy">
						<q-date v-model="expenseModel.date" minimal @update:model-value="$refs.datepickerProxy.hide()"></q-date>
					</q-popup-proxy>
				</q-icon>
			</template>
		</q-input>

		<q-input
			filled
			type="number"
			v-model="expenseModel.total_amount"
			label="Totaalprijs"
			mask="#.##"
		></q-input>

		<q-input
			filled
			type="number"
			v-model="expenseModel.debitors[inhabitant.id]"
			:label="inhabitant.nickname"
			v-for="inhabitant in inhabitantsStore.getInhabitants"
			:key="inhabitant.id"
			mask="#"
			dense
		></q-input>
	</q-form>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import {date} from 'quasar'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useExpenseCategoriesStore} from 'stores/expenseCategories'
import type {Expense} from '../models/Expense'
import type {Ref} from 'vue'

const expenseCategoriesStore = useExpenseCategoriesStore()
const inhabitantsStore = useInhabitantsStore()

let now = Date.now()

const expenseModel: Ref<Expense> = ref({
	date: date.formatDate(now, 'YYYY/MM/DD'),
	description: '',
	category: null,
	total_amount: null,
	debitors: [],
})

onMounted(() => {
	expenseCategoriesStore.fetch()
})

</script>

<style scoped>

</style>
