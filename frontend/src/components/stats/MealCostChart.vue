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

interface DataObject {
	inhabitant_id: number,
	avg_meal_cost: number,
}

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()

const {t} = useI18n()

const data = ref<DataObject[]>([])

const series = computed(() => [{
	data: data.value.toSorted((a, b) => b.avg_meal_cost - a.avg_meal_cost).map(x => {
		return {
			x: inhabitantsStore.inhabitants.find(inhabitant => inhabitant.id === x.inhabitant_id)?.nickname,
			y: x.avg_meal_cost,
		}
	}),
}])

const chartOptions = {
	chart: {
		type: 'bar',
		animations: {
			enabled: false,
		},
	},
	plotOptions: {
		bar: {
			horizontal: true
		}
	},
	xaxis: {
		decimalsInFloat: 2,
		title: {
			text: '€'
		}
	},
	title: {
		text: t('average_meal_cost_per_person')
	},
}

async function fetch() {
	const response = await authStore.request({
		url: 'stats/meal_cost',
		method: 'get',
	})

	data.value = response?.data
}

onMounted(() => {
	fetch()
})
</script>
