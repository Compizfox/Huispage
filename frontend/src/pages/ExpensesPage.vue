<template>
	<q-page class="q-gutter-y-md">
		<router-view></router-view>

		<div class="row q-gutter-md">
			<q-card
				v-for="inhabitant in getInhabitants" :key="inhabitant"
			>
				<q-item>
					<q-item-section avatar>
						<q-avatar>
							<img :src="inhabitant.avatar">
						</q-avatar>
					</q-item-section>

					<q-item-section>
						<q-item-label>{{ inhabitant.nickname }}</q-item-label>
						<q-item-label
							caption
							:class="{'text-positive': balance[inhabitant.id]>0,
					                 'text-negative': balance[inhabitant.id]<0 }"
						>
							€ {{ balance[inhabitant.id]?.toFixed(2) }}
						</q-item-label>
					</q-item-section>
				</q-item>
			</q-card>
		</div>

		<q-table
			dense
			:rows="rows"
			:columns="columns"
			:loading="loading"
			:filter="filter"
			row-key="id"
			v-model:pagination="pagination"
			:rows-per-page-options="[25, 50, 100, 0]"
			@request="onRequest"
		>
			<template #body-cell-category="props">
				<q-td :props="props">
					<q-icon
						:name="expenseCategoriesStore.expenseCategories.find(x => x.id === props.row.category).icon"
						size="2em">
						<q-tooltip>
							{{ expenseCategoriesStore.expenseCategories.find(x => x.id === props.row.category).name }}
						</q-tooltip>
					</q-icon>
				</q-td>
			</template>

			<template #body-cell-edit="props">
				<q-td :props="props">
					<router-link
						v-if="props.row.creditor_id === authStore.inhabitant?.id ||
						(authStore.inhabitant?.is_superuser && settingsStore.adminMode)"
						:to="{ name: 'expenseDetail', params: { id: props.row.id }}"
					>
						<q-icon name="edit"/>
					</router-link>
				</q-td>
			</template>

			<template v-for="inhabitantSlot in inhabitantSlots" #[inhabitantSlot]="props" :key="inhabitantSlot">
				<q-td :props="props">
					<q-badge
						:class="{ 'bg-deep-orange': props.col.name === props.row.creditor_name }"
						v-if="props.value || props.col.name === props.row.creditor_name"
					>
						{{ props.value }}
					</q-badge>
				</q-td>
			</template>

			<template #top-left>
				<div class="q-gutter-md row">
					<q-select
						filled
						clearable
						emit-value
						map-options
						:options="expenseCategoriesStore.expenseCategories"
						option-value="id"
						option-label="name"
						v-model="filter.category"
						:label="t('category')"
						style="width: 10em"
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
						filled
						clearable
						emit-value
						map-options
						:options="getInhabitants"
						option-value="id"
						option-label="nickname"
						v-model="filter.creditor"
						:label="t('creditor')"
						style="width: 10em"
					/>
					<q-checkbox
						v-model="settingsStore.showAllInhabitants"
						:label="t('show_all_inhabitants')"
					/>
					<q-checkbox
						v-if="authStore.inhabitant?.is_superuser"
						v-model="settingsStore.adminMode"
						:label="t('admin_mode')"
					/>
				</div>
			</template>
			<template #top-right>
				<router-link
					:to="{ name: 'createExpense' }"
				>
					<q-btn color="primary" :label="t('new')"/>
				</router-link>
			</template>
		</q-table>
	</q-page>
</template>

<script setup lang="ts">
import {onMounted, ref, computed} from 'vue'
import {date} from 'quasar'
import {onBeforeRouteUpdate} from 'vue-router'
import {useSettingsStore} from 'stores/settings'
import {useI18n} from 'vue-i18n'

import {useInhabitantsStore} from 'stores/inhabitants'
import {useExpenseCategoriesStore} from 'stores/expenseCategories'
import {useAuthStore} from 'stores/auth'

import type {Expense} from 'src/models/Expense'
import type {QTableProps} from 'quasar'
import type {Ref} from 'vue'

const {t} = useI18n()
const inhabitantsStore = useInhabitantsStore()
const expenseCategoriesStore = useExpenseCategoriesStore()
const authStore = useAuthStore()
const settingsStore = useSettingsStore()

const balance = ref({})
const loading = ref(true)
const rows: Ref<Array<Expense>> = ref([])
const pagination = ref({
	sortBy: 'date',
	descending: true,
	page: 1,
	rowsPerPage: 25,
	rowsNumber: 0,
})
const filter = ref({
	category: null,
	creditor: null,
})

const columns = computed(() => [
	{
		name: 'category',
		required: true,
		label: '',
		align: 'center',
		sortable: true,
		field: (row: Expense) => row.category,
	},
	{
		name: 'updated_at',
		required: true,
		label: t('added_at'),
		sortable: true,
		field: (row: Expense) => row.updated_at,
		format: (val: string) => date.formatDate(val, 'YYYY-MM-DD'),
	},
	{
		name: 'date',
		required: true,
		label: t('date'),
		align: 'left',
		sortable: true,
		field: (row: Expense) => row.date,
		format: (val: string) => date.formatDate(val, 'YYYY-MM-DD'),
	},
	{
		name: 'description',
		required: true,
		label: t('description'),
		align: 'left',
		field: (row: Expense) => row.description,
	},
	{
		name: 'total_amount',
		required: true,
		label: t('total'),
		align: 'right',
		field: (row: Expense) => row.total_amount,
		format: (val: number) => (val ?? 0).toFixed(2),
	},
	{
		name: 'unit_price',
		required: true,
		label: 'pp',
		align: 'right',
		field: (row: Expense) => row.unit_price,
		format: (val: number) => (val ?? 0).toFixed(2),
	}
].concat(getInhabitants.value.map((inhabitant) => {
	return {
		name: inhabitant.username,
		required: true,
		label: inhabitant.nickname,
		align: 'center',
		field: row => row.debitors.find(x => x.inhabitant === inhabitant.id)?.amount,
		format: val => (val ?? 0)
	}
})).concat([
	{
		name: 'edit',
		required: true,
		label: '',
		align: 'center',
	},
]))

expenseCategoriesStore.fetch()
inhabitantsStore.fetch()

authStore.request({
	url: 'balance/',
	method: 'get',
}).then(response => {
	balance.value = response?.data
})

fetch()

// Generate list of names of body cell slots for the debitor columns
const inhabitantSlots = computed(() =>
	getInhabitants.value.map(inhabitant => 'body-cell-' + inhabitant.username)
)

const getInhabitants = computed(() =>
	settingsStore.showAllInhabitants ? inhabitantsStore.inhabitants : inhabitantsStore.getCurrentInhabitants
)

const onRequest: QTableProps['onRequest'] = (requestProp) => {
	pagination.value = Object.assign(pagination.value, requestProp.pagination);
	fetch()
}

async function fetch() {
	loading.value = true

	let response = await authStore.request({
		url: 'expenses/',
		method: 'get',
		params: {
			category: filter.value.category,
			creditor: filter.value.creditor,
			ordering: (pagination.value.descending? '-' : '') + pagination.value.sortBy,
			page: pagination.value.page,
			page_size: pagination.value.rowsPerPage,
		}
	})

	pagination.value.rowsNumber = response?.data.count
	rows.value = response?.data.results

	loading.value = false
}

onBeforeRouteUpdate(() => {
	fetch()
})
</script>
