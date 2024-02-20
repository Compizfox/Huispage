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
				:label="t('category')"
				:error="v.category.$error"
				hide-bottom-space
				:disable="readOnly"
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
				emit-value
				map-options
				:options="inhabitantsStore.getCurrentInhabitants"
				option-value="id"
				option-label="nickname"
				v-model="expense.creditor_id"
				:label="t('creditor')"
				:error="v.creditor_id.$error"
				hide-bottom-space
				:disable="readOnly"
			/>

			<q-input
				outlined
				v-model="expense.description"
				:label="t('description')"
				:error="v.description.$error"
				hide-bottom-space
				:disable="readOnly"
			/>

			<DateInput
				v-model="expense.date"
				:label="t('date')"
				:error="v.date.$error"
				:disable="readOnly"
			/>

			<q-input
				outlined
				type="number"
				v-model="expense.total_amount"
				:label="t('total_price')"
				mask="#.##"
				prefix="€"
				:error="v.total_amount.$error"
				hide-bottom-space
				:disable="readOnly"
			/>

			<q-field
				outlined
				:error="v.debitors.$error"
				hide-bottom-space
			>
				<div class="row q-gutter-md q-py-sm">
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
						:disable="disable(debitor.inhabitant)"
					/>
				</div>
			</q-field>
		</q-card-section>
	</q-form>
</template>

<script setup lang="ts">
import {useInhabitantsStore} from 'stores/inhabitants'
import {useExpenseCategoriesStore} from 'stores/expenseCategories'
import type {Expense} from 'src/models/Expense'
import {useAuthStore} from 'stores/auth'
import {useI18n} from 'vue-i18n'
import DateInput from 'components/DateInput.vue'
import {useVuelidate} from '@vuelidate/core'
import {required, numeric, integer, minValue, helpers} from '@vuelidate/validators'

const {t} = useI18n()
const expenseCategoriesStore = useExpenseCategoriesStore()
const inhabitantsStore = useInhabitantsStore()
const authStore = useAuthStore()

const expense = defineModel<Expense>({required: true})

const props = defineProps<{
	readOnly: boolean
	publiclyEditableAmount: boolean
}>()

function disable(inhabitant: number) {
	if(props.readOnly) {
		return !(authStore.inhabitant!.id === inhabitant && props.publiclyEditableAmount)
	} else {
		return false
	}
}


const validations = {
	category: { required, integer },
	creditor_id: {required, integer },
	description: { required },
	date: { required },
	total_amount: {
		required,
		numeric,
		minValueValue: minValue(0),
	},
	debitors: {
		$each: helpers.forEach({
			inhabitant: { required, integer },
			amount: {
				numeric,
				minValueValue: minValue(0)
			}
		}),
	debitorSum: ((debitors: Expense['debitors']) =>
		debitors.map((debitor) => debitor.amount).reduce((sum, cur) => sum + cur) > 0)
	}
}

const v = useVuelidate(validations, expense, {$lazy: true, $autoDirty: true})

async function validate() {
	return await v.value.$validate()
}

defineExpose({
	validate
})
</script>

<style scoped>

</style>
