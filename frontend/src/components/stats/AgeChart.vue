<template>
	<q-card>
		<q-card-section>
			<div class="text-h4">{{ t('age_stats')}}</div>
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

interface DataObject {
	yearmonth: string,
	avg_age: number,
	min_age: number,
	max_age: number,
}

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const {t} = useI18n()

const data = ref<DataObject[]>([])

const series = computed(() => [
	{
		type: 'rangeArea',
		name: 'Range',
		data: data.value.map(x => {
			return {
				x: x.yearmonth,
				y: [x.min_age, x.max_age],
			}
		}),
	},
	{
		type: 'line',
		name: 'Average',
		data: data.value.map(x => {
			return {
				x: x.yearmonth,
				y: x.avg_age,
			}
		}),
	}
],)

const chartOptions = computed(() => {
	return {
		chart: {
			type: 'rangeArea',
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
			stepSize: 2,
			decimalsInFloat: 2,
			title: {
				text: t('year')
			}
		},
		dataLabels: {
			enabled: false
		},
		fill: {
			opacity: [0.25, 1]
		},
		stroke: {
			curve: 'straight',
			width: [0, 3],
		},
		markers: {
			hover: {
				sizeOffset: 5
			}
		},
		tooltip: {
			x: {
				format: 'dd MMM yyyy',
			},
		},
		annotations: {
			xaxis: inhabitantsStore.inhabitants.map(inhabitant => {
				return {
					x: new Date(inhabitant.date_entrance).getTime(),
					label: {
						text: inhabitant.nickname,
						borderWidth: 0,
						position: 'bottom',
					}
				}
			})
		},
		title: {
			text: t('average_inhabitant_age')
		}
	}
})

async function fetch() {
	const response = await authStore.request({
		url: 'stats/inhabitant_dob_stats',
		method: 'get',
	})

	data.value = response?.data
}

onMounted(() => {
	fetch()
})
</script>
