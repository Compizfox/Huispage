<template>
	<q-page>
		<router-view></router-view>

		<q-table
			dense
			:rows="rows"
			:columns="columns"
			:loading="loading"
			:filter="filter"
			row-key="id"
			v-model:pagination="pagination"
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
						v-if="props.row.creditor_id === authStore.inhabitant?.id || authStore.inhabitant?.is_superuser"
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
						v-if="props.value"
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
						label="Category filter"
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
						label="Creditor"
						style="width: 10em"
					/>
					<q-checkbox
						v-model="settingsStore.showAllInhabitants"
						label="Show all inhabitants"
					/>

				</div>
			</template>
			<template #top-right>
				<router-link
					:to="{ name: 'createExpense' }"
				>
					<q-btn color="primary" label="Nieuw"/>
				</router-link>
			</template>
		</q-table>
	</q-page>
</template>

<script setup>
import {onMounted, ref, computed} from 'vue'
import {date} from 'quasar'
import {useInhabitantsStore} from 'stores/inhabitants.ts'
import {useExpenseCategoriesStore} from 'stores/expenseCategories.ts'
import {useAuthStore} from 'stores/auth'
import {onBeforeRouteUpdate} from 'vue-router'
import {useSettingsStore} from 'stores/settings'

const inhabitantsStore = useInhabitantsStore()
const expenseCategoriesStore = useExpenseCategoriesStore()
const authStore = useAuthStore()
const settingsStore = useSettingsStore()

const loading = ref(true)
const rows = ref([])
const pagination = ref({
	sortBy: 'desc',
	descending: false,
	page: 1,
	rowsPerPage: 3,
	rowsNumber: 10
})

const columns = computed(() => [
	{
		name: 'category',
		required: true,
		label: '',
		align: 'center',
		field: row => row.category,
	},
	{
		name: 'date',
		required: true,
		label: 'Datum',
		align: 'left',
		field: row => row.date,
		format: val => date.formatDate(val, 'YYYY-MM-DD'),
	},
	{
		name: 'description',
		required: true,
		label: 'Description',
		align: 'left',
		field: row => row.description,
	},
	{
		name: 'total_amount',
		required: true,
		label: 'Total',
		align: 'right',
		field: row => row.total_amount,
		format: val => (val ?? 0).toFixed(2),
	},
	{
		name: 'unit_price',
		required: true,
		label: 'pp',
		align: 'right',
		field: row => row.unit_price,
		format: val => (val ?? 0).toFixed(2),
	}
].concat(getInhabitants.value.map((inhabitant) => {
	return {
		name: inhabitant.username,
		required: true,
		label: inhabitant.nickname,
		align: 'right',
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

const filter = ref({
	category: null,
	creditor: null,
})

const getInhabitants = computed(() =>
	settingsStore.showAllInhabitants ? inhabitantsStore.inhabitants : inhabitantsStore.getCurrentInhabitants
)

function onRequest(props) {
	loading.value = true

	fetch()
}

// Generate list of names of body cell slots for the debitor columns
const inhabitantSlots = computed(() =>
	getInhabitants.value.map(inhabitant => 'body-cell-' + inhabitant.username)
)

function fetch() {
	authStore.request({
		url: 'expenses/',
		method: 'get',
		params: {
			category: filter.value.category,
			creditor: filter.value.creditor,
		}
	}).then(response => {
		rows.value = response?.data
	}).finally(() => {
		loading.value = false
	})
}

onMounted(() => {
	expenseCategoriesStore.fetch()
	inhabitantsStore.fetch()

	fetch()
})

onBeforeRouteUpdate(async (to, from) => {
	fetch()
})
</script>
