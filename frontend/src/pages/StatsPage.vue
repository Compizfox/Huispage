<template>
	<q-page padding>
		<q-checkbox
			v-model="settingsStore.showAllInhabitants"
			:label="t('show_all_inhabitants')"
		/>
		<div class="row">
			<div class="col-xs-12 col-md-6 col-xl-4">
				<OccupancyChart/>
			</div>
			<div class="col-xs-12 col-md-6 col-xl-4">
				<AgeChart/>
			</div>
			<div class="col-xs-12 col-md-6 col-xl-4">
				<MealCostCard/>
			</div>
			<div class="col-xs-12 col-md-6 col-xl-4">
				<MealChart/>
			</div>
			<div class="col-xs-12 col-md-6 col-xl-4">
				<EnrolmentChart/>
			</div>
			<div class="col-xs-12 col-md-6 col-xl-4">
				<MealStatsCard/>
			</div>
			<div class="col-xs-12 col-md-6 col-xl-4">
				<ExpenseChart/>
			</div>
		</div>
	</q-page>
</template>

<script setup lang="ts">
import OccupancyChart from 'components/stats/OccupancyChart.vue'
import MealCostCard from 'components/stats/MealCostCard.vue'
import MealChart from 'components/stats/MealChart.vue'
import AgeChart from 'components/stats/AgeChart.vue'
import EnrolmentChart from 'components/stats/EnrolmentChart.vue'
import MealStatsCard from 'components/stats/MealStatsCard.vue'
import ExpenseChart from 'components/stats/ExpenseChart.vue'

import {useI18n} from 'vue-i18n'
import {useSettingsStore} from 'stores/settings'

const {t} = useI18n()
const settingsStore = useSettingsStore()
</script>

<style scoped>
.q-card {
	margin: 5px;
}
</style>
