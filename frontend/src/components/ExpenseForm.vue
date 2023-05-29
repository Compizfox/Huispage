<template>
	<q-form>
		<q-card-section class="q-gutter-md">
			<q-select
				outlined
				emit-value
				map-options
				:options="expenseCategoriesStore.expenseCategories"
				option-value="id"
				option-label="name"
				v-model="expense.category"
				label="Categorie"
			>
				<template #option="scope">
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

			<q-select
				outlined
				v-if="authStore.inhabitant?.is_superuser"
				emit-value
				map-options
				:options="inhabitantsStore.getCurrentInhabitants"
				option-value="id"
				option-label="nickname"
				v-model="expense.creditor_id"
				label="Creditor"
			/>

			<q-input
				outlined
				v-model="expense.description"
				label="Omschrijving"
			/>

			<q-input
				outlined
				v-model="expense.date"
				mask="####-##-##"
				fill-mask
				hide-bottom-space
			>
				<template #append>
					<q-icon name="event" class="cursor-pointer">
						<q-popup-proxy ref="datepickerProxy">
							<q-date
								v-model="expense.date" minimal
								@update:model-value="$refs.datepickerProxy.hide()"
								today-btn
							/>
						</q-popup-proxy>
					</q-icon>
				</template>
			</q-input>

			<q-input
				outlined
				type="number"
				v-model="expense.total_amount"
				label="Totaalprijs"
				mask="#.##"
			/>

			<div class="row q-gutter-md">
				<q-input
					v-for="debitor in expense.debitors"
					:key="debitor.inhabitant"
					outlined
					type="number"
					v-model="debitor.amount"
					:label="inhabitantsStore.inhabitants.find(x => x.id === debitor.inhabitant).nickname"
					mask="#"
					dense
					class="col-2"
				/>
			</div>
		</q-card-section>
	</q-form>
</template>

<script setup lang="ts">
import {onMounted, computed} from 'vue'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useExpenseCategoriesStore} from 'stores/expenseCategories'
import type {Expense} from '../models/Expense'
import {useAuthStore} from 'stores/auth'

const expenseCategoriesStore = useExpenseCategoriesStore()
const inhabitantsStore = useInhabitantsStore()
const authStore = useAuthStore()

// For component v-model
const props = defineProps<{ modelValue: Expense }>()
const emit = defineEmits(['update:modelValue', 'onSubmit'])

const expense = computed({
	get() {
		return props.modelValue
	},
	set(value) {
		emit('update:modelValue', expense)
	}
})
</script>

<style scoped>

</style>
