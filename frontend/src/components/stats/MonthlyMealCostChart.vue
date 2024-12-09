<template>
	<apexchart
		:series="series"
		:options="chartOptions"
	/>
</template>

<script setup lang="ts">
import {onMounted, computed, ref} from 'vue'
import {useI18n} from 'vue-i18n'
import {useAuthStore} from 'stores/auth'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useSettingsStore} from 'stores/settings'

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const settingsStore = useSettingsStore()
const {t} = useI18n()

const data = ref<[string, [string, number][]][]>([])

const series = computed(() =>
	data.value.map(([k, v]) => {
		return {
			name: inhabitantsStore.inhabitants.find(x => x.id === Number(k))?.nickname,
			data: v
		}
	})
)

const chartOptions = computed(() => {
	return {
		chart: {
			type: 'line',
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
		yaxis: {
			decimalsInFloat: 2,
			title: {
				text: '€'
			}
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
		markers: {
			size: 5
		},
		title: {
			text: t('average_meal_cost_per_person')
		},
	}
})

async function fetch() {
	const response = await authStore.request({
		url: 'stats/monthly_meal_cost',
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
