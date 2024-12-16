<template>
	<q-card>
		<q-card-section>
			<div class="text-h4">{{ t('expense_stats')}}</div>
		</q-card-section>
		<q-card-section>
			<q-select
				outlined
				emit-value
				map-options
				:options="expenseCategoriesStore.expenseCategories"
				option-value="id"
				option-label="name"
				v-model="category"
				:label="t('category')"
				hide-bottom-space
				@update:model-value="fetch"
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
		</q-card-section>
		<q-card-section>
			<apexchart
				:series="series"
				:options="chartOptions"
			/>
		</q-card-section>
	</q-card>
</template>

<script setup lang="ts">
import {onMounted, computed, ref} from 'vue'
import {useI18n} from 'vue-i18n'
import {useAuthStore} from 'stores/auth'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useSettingsStore} from 'stores/settings'
import {useExpenseCategoriesStore} from 'stores/expenseCategories'

const {t} = useI18n()

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const settingsStore = useSettingsStore()
const expenseCategoriesStore = useExpenseCategoriesStore()

const category = ref(3)
const data = ref<[string, [string, number][]][]>([])

const series = computed(() =>
	data.value
		// Filter out non-current inhabitants
		.filter(([k, v]) =>
			settingsStore.showAllInhabitants || inhabitantsStore.getCurrentInhabitants.some(inhabitant => inhabitant.id === Number(k))
		)
		.map(([k, v]) => {
			return {
				name: inhabitantsStore.inhabitants.find(inhabitant => inhabitant.id === Number(k))?.nickname,
				data: v
			}
		})
)

const chartOptions = computed(() => {
	return {
		chart: {
			type: 'bar',
			stacked: 'true',
			animations: {
				enabled: false,
			},
			zoom: {
				allowMouseWheelZoom: false,
			}
		},
		xaxis: {
			type: 'datetime'
		},
		dataLabels: {
			enabled: false
		},
		tooltip: {
			x: {
				format: 'dd MMM yyyy',
			},
		},
		stroke: {
			width: 2.5,
			curve: 'smooth'
		},
		title: {
			text: t('expense_cost_per_month')
		}
	}
})

async function fetch() {
	const response = await authStore.request({
		url: 'stats/expense_stats/' + category.value,
		method: 'get',
	})

	// Convert object to array
	data.value = response?.data
}

onMounted(() => {
	expenseCategoriesStore.fetch()
	fetch()
})
</script>
