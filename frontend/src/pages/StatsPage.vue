<template>
	<q-page padding>
		<q-card>
			<q-card-section>
				<div class="text-h4">{{ t('inhabitant_occupancy')}}</div>
			</q-card-section>
			<q-card-section>
				<apexchart
					type="rangeBar"
					:series="series"
					:options="chartOptions"
				/>
			</q-card-section>
		</q-card>
	</q-page>
</template>

<script setup lang="ts">
import {date} from 'quasar'
import {useInhabitantsStore} from 'stores/inhabitants'
import {onMounted, computed} from 'vue'
import {useI18n} from 'vue-i18n';

const inhabitantsStore = useInhabitantsStore()
const {t} = useI18n()


const series = computed(() => [
	{
		data: inhabitantsStore.inhabitants.map(inhabitant => {
			return {
				x: inhabitant.nickname,
				y: [
					new Date(inhabitant.date_entrance).getTime(),
					inhabitant.date_leave? new Date(inhabitant.date_leave).getTime() : new Date().getTime(),
				],
			}
		}),
	}
])

const chartOptions = {
	chart: {
		type: 'rangeBar',
		animations: {
			enabled: false,
		},
		toolbar: {
			show: false,
		},
		zoom: {
			enabled: false,
		}
	},
	dataLabels: {
		enabled: true,
		formatter: (val: Date[]) => {
			return date.getDateDiff(val[1], val[0], 'months') + t(' months')
		}
	},
	plotOptions: {
		bar: {
			horizontal: true
		}
	},
	xaxis: {
		type: 'datetime'
	},
}

onMounted(() => {
	inhabitantsStore.fetch()
})
</script>
