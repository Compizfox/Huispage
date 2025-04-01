<template>
	<q-form>
		<q-card-section class="q-col-gutter-md row">
			<q-select
				class="col-12 col-sm-6"
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
				class="col-12 col-sm-6"
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
				class="col-12 col-sm-6"
				outlined
				v-model="expense.description"
				:label="t('description')"
				:error="v.description.$error"
				hide-bottom-space
				:disable="readOnly"
			/>

			<DateInput
				class="col-12 col-sm-6"
				v-model="expense.date"
				:label="t('date')"
				:error="v.date.$error"
				:disable="readOnly"
			/>

			<div class="col-12 row justify-end">
				<q-btn-group>
					<q-btn
						color="secondary"
						no-caps
						@click="setDebitorAmounts(0)"
					>
						{{  t('all_to_0') }}
					</q-btn>
					<q-btn
						color="secondary"
						no-caps
						@click="setDebitorAmounts(1)"
					>
						{{ t('all_to_1') }}
					</q-btn>
				</q-btn-group>
			</div>

			<q-field
				class="col-12"
				outlined
				:error="v.debitors.$error"
				hide-bottom-space
				dense
			>
				<div
					class="responsive-grid col q-col-gutter-x-lg q-col-gutter-y-sm q-py-md"
				>
					<div
						v-for="debitor in expense.debitors"
						:key="debitor.inhabitant"
						class="row no-wrap q-col-gutter-x-md items-center"
					>
						<div style="flex-grow: 1">
							<q-chip>
								{{ inhabitantsStore.inhabitants.find(x => x.id === debitor.inhabitant).nickname }}
							</q-chip>
						</div>

						<div>
							<q-btn-group rounded dense>
								<q-btn
									@click="debitor.amount--"
									icon="remove"
									padding="6px"
								/>
								<q-input
									borderless
									type="number"
									v-model.number="debitor.amount"
									mask="#"
									:disable="disable(debitor.inhabitant)"
									size="1"
								/>
								<q-btn
									@click="debitor.amount++"
									icon="add"
									padding="6px"
								/>
							</q-btn-group>
						</div>
					</div>
				</div>
			</q-field>

			<div>
				<ExpenseItemsTable v-model="expense.items"/>
			</div>

			<div class="row col-12 items-center justify-between">
				<q-input
					outlined
					type="number"
					v-model.number="expense.total_amount"
					:label="t('total_price')"
					mask="#.##"
					prefix="€"
					:error="v.total_amount.$error"
					hide-bottom-space
					:disable="readOnly || expense.items.length > 1"
					class="col"
				/>
				<span class="q-pa-sm">/</span>
				<q-input
					outlined
					:model-value="debitorSum"
					readonly
					size="2"
				/>
				<span class="q-pa-sm">=</span>
				<q-input
					outlined
					stack-label
					:label="t('price_per_person')"
					prefix="€"
					:model-value="(expense.total_amount / debitorSum).toFixed(2)"
					readonly
					class="col"
				/>
			</div>

			<div
				class="col-12"
				v-if="showCookWarning"
			>
				<q-banner
					rounded
					class="bg-warning"
				>
					{{ t('not_cook_warning') }}
				</q-banner>
			</div>
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
import {helpers, integer, minValue, not, numeric, required, sameAs} from '@vuelidate/validators'
import {computed, ref, watch} from 'vue'
import ExpenseItemsTable from 'components/ExpenseItemsTable.vue'

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

function setDebitorAmounts(n: number) {
	expense.value.debitors.forEach((debitor) => {
		debitor.amount = n
	})
}

const cook = ref<number | null | undefined>(undefined)

const showCookWarning = computed(() => {
	return expense.value.category === 1 && cook.value !== undefined && cook.value != expense.value.creditor_id
})

async function fetchCook(date: string): Promise<number | null> {
	const response = await authStore.request({
		url: 'meals/?date=' + date,
		method: 'get',
	})

	return response?.data[0]?.cook ?? null
}

const debitorSum = computed(() => {
	return expense.value.debitors.map((debitor) => debitor.amount).reduce((sum, cur) => sum + cur)
})

const itemsDefined = computed(() => {
	return expense.value.items.some((item) => item.name != '' || item.cost != 0)
})

const dateRegex = helpers.regex(/^\d{4}-([0][1-9]|1[0-2])-([0][1-9]|[1-2]\d|3[01])$/)

const validations = {
	category: {required, integer},
	creditor_id: {required, integer},
	description: {required},
	date: {required, dateRegex},
	total_amount: {
		required,
		numeric,
		minValueValue: minValue(0),
		sameAsRawValue: not(sameAs(0)),
	},
	debitors: {
		$each: helpers.forEach({
			inhabitant: {required, integer},
			amount: {
				numeric,
				minValueValue: minValue(0)
			}
		}),
		debitorSum: ((debitors: Expense['debitors']) =>
			debitors.map((debitor) => debitor.amount).reduce((sum, cur) => sum + cur) > 0)
	},
}

const v = useVuelidate(validations, expense, {$lazy: true, $autoDirty: true})

watch(
	() => expense.value.date,
	async (date) => {
		v.value.date.$touch()
		if (!v.value.date.$invalid) {
			cook.value = await fetchCook(date)
		}
	},
	{immediate: true}
)

watch(
	() => expense.value.items,
	() => {
		expense.value.total_amount = expense.value.items.reduce((n, {cost}) => n + cost, 0)
	},
	{deep: true}
)

async function validate() {
	return await v.value.$validate()
}

defineExpose({
	validate
})
</script>

<style scoped lang="scss">
.responsive-grid {
	display: grid;
	justify-content: space-between;
	@media (min-width: 600px) {
		grid-template-columns: repeat(2, minmax(max-content, 1fr));
	}
}
</style>
