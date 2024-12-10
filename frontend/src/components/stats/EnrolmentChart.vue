<template>
	<q-card>
		<q-card-section>
			<div class="text-h4">{{ t('enrolment_stats')}}</div>
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

interface DataObject {
	yearmonth: string,
	meal_count: number,
	enrolment_count: number,
	ratio: number,
}

const {t} = useI18n()

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const settingsStore = useSettingsStore()

const data = ref<[string, DataObject[]][]>([])

const series = computed(() =>
	data.value.map(([k, v]) => {
		return {
			name: inhabitantsStore.inhabitants.find(inhabitant => inhabitant.id === Number(k))?.nickname,
			data: v.map(x => {
				return {
					x: x.yearmonth,
					y: x.enrolment_count,
				}
			})
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
			text: t('number_enrolments_per_month')
		}
	}
})

async function fetch() {
	const response = await authStore.request({
		url: 'stats/monthly_meal_stats',
		method: 'get',
	})

	// Convert object to array
	data.value = Object.entries(response?.data)

	if (!settingsStore.showAllInhabitants) {
		// Filter out non-current inhabitants
		data.value = data.value.filter(([k, v]) =>
			inhabitantsStore.getCurrentInhabitants.some(inhabitant => inhabitant.id === Number(k))
		)
	}
}

onMounted(() => {
	fetch()
})
</script>
