<template>
	<q-table
		:rows="model"
		:columns="columns"
		:rows-per-page-options="[0]"
		hide-header
		hide-bottom
		:title="t('items')"
		title-class="text-h6"
	>
		<template v-slot:body="props">
			<ExpenseItemRow v-model="model[props.rowIndex]" @delete="deleteItem(props.rowIndex)"/>
		</template>
	</q-table>
</template>

<script setup lang="ts">
import {watch} from 'vue'
import {useI18n} from 'vue-i18n'
import {useVuelidate} from '@vuelidate/core'
import ExpenseItemRow from 'components/ExpenseItemRow.vue'
import type {ExpenseItem} from 'components/ExpenseItemRow.vue'

const {t} = useI18n()

const model = defineModel<ExpenseItem[]>({required: true})

const columns = [
	{
		name: 'name',
		label: t('name'),
		field: (row: ExpenseItem) => row.name,
	},
	{
		name: 'cost',
		label: t('price'),
		field: (row: ExpenseItem) => row.cost,
	},
	{
		name: 'actions',
		label: '',
		align: 'center',
	},
]

function deleteItem(index: number) {
	// Don't delete last item
	if (model.value.length == 1) return

	model.value.splice(index, 1)
}

watch(
	() => model.value,
	() => {
		let lastRow = model.value[model.value.length - 1]
		if (lastRow.name != '' || lastRow.cost != 0) {
			model.value.push({name: '', cost: 0})
		}
	},
	{deep: true}
)

const v = useVuelidate()
</script>
