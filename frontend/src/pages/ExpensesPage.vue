<template>
	<q-page padding>
		<router-view></router-view>

		<div class="row q-gutter-md q-mb-md">
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
			<template #body="props">
				<q-tr :props="props">
					<!-- category -->
					<q-td class="text-center">
						<q-icon
							:name="expenseCategoriesStore.expenseCategories.find(x => x.id === props.row.category)!.icon"
							size="2em">
							<q-tooltip>
								{{ expenseCategoriesStore.expenseCategories.find(x => x.id === props.row.category)!.name }}
							</q-tooltip>
						</q-icon>
					</q-td>

					<!-- updated_at -->
					<q-td class="text-left">
						{{ props.cols[1].value }}
					</q-td>

					<!-- date -->
					<q-td class="text-left">
						{{ props.cols[2].value }}
					</q-td>

					<!-- description -->
					<q-td class="text-left">
						<div class="row justify-between">
							{{ props.cols[3].value }}
							<q-btn
								size="xs"
								dense
								@click="props.expand = !props.expand"
								:icon="props.expand ? 'unfold_less' : 'unfold_more'"
								v-if="props.row.items.length > 0"
							/>
						</div>
					</q-td>

					<!-- total_amount -->
					<q-td class="text-right">
						{{ props.cols[4].value }}
					</q-td>

					<!-- unit_price -->
					<q-td class="text-right">
						{{ props.cols[5].value }}
					</q-td>

					<template v-for="inhabitant in getInhabitants" :key="inhabitant">
						<q-td class="text-center">
							<q-badge
								:class="{'bg-deep-orange': inhabitant.id === props.row.creditor_id}"
								v-if="props.row.debitors.find(x => x.inhabitant === inhabitant.id).amount > 0 ||
								inhabitant.id === props.row.creditor_id"
							>
								{{ props.row.debitors.find(x => x.inhabitant === inhabitant.id)?.amount }}
							</q-badge>
						</q-td>
					</template>

					<q-td>
						<router-link :to="{ name: 'expenseDetail', params: { id: props.row.id }}">
							<q-icon name="open_in_new"/>
						</router-link>
					</q-td>
				</q-tr>
				<q-tr
					v-for="(item, index) in props.row.items"
					v-show="props.expand"
					:props="props"
					class="item-row"
				>
					<q-td :class="{'hide-border': index !== props.row.items.length -1}"/>
					<q-td :class="{'hide-border': index !== props.row.items.length -1}"/>
					<q-td
						:class="{'hide-border': index !== props.row.items.length -1}"
						class="border-right"
					/>
					<q-td class="text-left">
						{{ item.name }}
					</q-td>
					<q-td class="text-right">
						{{ item.cost.toFixed(2) }}
					</q-td>
					<q-td :class="{'hide-border': index !== props.row.items.length -1}"/>
					<q-td
						v-for="inhabitant in getInhabitants"
						:class="{'hide-border': index !== props.row.items.length -1}"
					/>
					<q-td :class="{'hide-border': index !== props.row.items.length -1}"/>
				</q-tr>
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
import {ref, computed} from 'vue'
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
		align: 'left',
		sortable: true,
		sortOrder: 'da',
		field: (row: Expense) => row.updated_at,
		format: (val: string) => date.formatDate(val, 'YYYY-MM-DD'),
	},
	{
		name: 'date',
		required: true,
		label: t('date'),
		align: 'left',
		sortable: true,
		sortOrder: 'da',
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
settingsStore.fetch()

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

	// Fetch expenses
	authStore.request({
		url: 'expenses/',
		method: 'get',
		params: {
			category: filter.value.category,
			creditor: filter.value.creditor,
			ordering: (pagination.value.descending? '-' : '') + pagination.value.sortBy,
			page: pagination.value.page,
			page_size: pagination.value.rowsPerPage,
		}
	}).then(response => {
		pagination.value.rowsNumber = response?.data.count
		rows.value = response?.data.results
		loading.value = false
	})

	// Fetch balances
	authStore.request({
		url: 'balance/',
		method: 'get',
	}).then(response => {
		balance.value = response?.data
	})
}

onBeforeRouteUpdate(() => {
	fetch()
})
</script>

<style scoped>
tr.item-row {
	height: unset !important;
}

.item-row td {
	padding: 0 8px;
	height: unset !important;
}

.item-row td.hide-border {
	border-bottom: 0;
}

.item-row td.border-right {
	border-right: 1px solid lightgray;
}
</style>
