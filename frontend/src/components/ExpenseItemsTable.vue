<template>
	<q-table
		:rows="model"
		:columns="columns"
		:rows-per-page-options="[0]"
		hide-bottom
		dense
	>
		<template #top>
			<div class="text-h6">
				<q-icon name="list"/>
				{{ t('items') }}
			</div>
		</template>
		<template #body="props">
			<ExpenseItemRow
				v-model="model[props.rowIndex]"
				@delete="deleteItem(props.rowIndex)"
				:readOnly="readOnly"
			/>
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

const props = defineProps<{
	readOnly: boolean
}>()

const columns = [
	{
		name: 'name',
		label: t('name'),
		field: (row: ExpenseItem) => row.name,
		align: 'left',
	},
	{
		name: 'cost',
		label: t('price'),
		field: (row: ExpenseItem) => row.cost,
		align: 'left',
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
