<template>
  <q-table
      :rows="model"
      :columns="columns"
	  :rows-per-page-options="[0]"
	  hide-header
	  hide-bottom
  >
    <template v-slot:body-cell-name="props">
      <q-td :props="props">
        <q-input
            outlined
            :label="t('description')"
            hide-bottom-space
            v-model="props.row.name"
            dense
        />
      </q-td>
    </template>
    <template v-slot:body-cell-cost="props">
      <q-td :props="props">
        <q-input
            outlined
            type="number"
            v-model.number="props.row.cost"
            :label="t('price')"
            mask="#.##"
            prefix="€"
            hide-bottom-space
            dense
        />
      </q-td>
    </template>
    <template v-slot:body-cell-actions="props">
		<q-td :props="props">
			<q-btn
				icon="close"
				dense
				@click="deleteItem(props.row)"
			/>
		</q-td>
    </template>
  </q-table>
</template>

<script setup lang="ts">
import {watch} from 'vue'
import {useI18n} from 'vue-i18n'

const {t} = useI18n()

interface ExpenseItem {
	name: string,
	cost: number,
}

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

function deleteItem(item: ExpenseItem) {
	if (model.value.length == 1) return

	model.value.splice(model.value.indexOf(item), 1)
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
</script>
