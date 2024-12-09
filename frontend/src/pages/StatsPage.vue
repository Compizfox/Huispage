<template>
	<q-page padding>
		<div class="row">
			<div class="col-xs-12 col-sm-6 col-xl-4">
				<OccupancyChart/>
			</div>
			<div class="col-xs-12 col-sm-6 col-xl-4">
				<AgeChart/>
			</div>
			<div class="col-xs-12 col-sm-6 col-xl-4">
				<MealCostCard/>
			</div>
			<div class="col-xs-12 col-sm-6 col-xl-4">
				<MealChart/>
			</div>
			<div class="col-xs-12 col-sm-6 col-xl-4">
				<EnrolmentChart/>
			</div>
			<div class="col-xs-12 col-sm-6 col-xl-4">
				<MealStatsCard/>
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
</script>

<style scoped>
.q-card {
	margin: 5px;
}
</style>
