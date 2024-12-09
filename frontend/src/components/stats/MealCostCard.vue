<template>
	<q-card>
		<q-card-section>
			<div class="text-h4">{{ t('meal_cost')}}</div>
		</q-card-section>
		<q-tabs v-model="tab" class="text-teal">
			<q-tab :label="t('total')" name="total"/>
			<q-tab :label="t('monthly')" name="monthly"/>
		</q-tabs>
		<q-separator/>
		<q-tab-panels v-model="tab" animated>
			<q-tab-panel name="total">
				<MealCostChart/>
			</q-tab-panel>
			<q-tab-panel name="monthly">
				<MonthlyMealCostChart/>
			</q-tab-panel>
		</q-tab-panels>
	</q-card>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import {useI18n} from 'vue-i18n'

import MealCostChart from 'components/stats/MealCostChart.vue'
import MonthlyMealCostChart from 'components/stats/MonthlyMealCostChart.vue'

const {t} = useI18n()
const tab = ref('total')
</script>

<style scoped lang="scss">

</style>
