<template>
	<q-card>
		<q-card-section>
			<div class="text-h4">{{ t('meal_cost')}}</div>
		</q-card-section>
		<q-card-section>
			<q-select
				filled
				clearable
				emit-value
				map-options
				:options="expenseCategoriesStore.expenseCategories"
				option-value="id"
				option-label="name"
				v-model="category"
				label="Category"
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
			<apexchart
				type="bar"
				:series="series"
				:options="chartOptions"
			/>
		</q-card-section>
	</q-card>
</template>

<script setup lang="ts">
import {date} from 'quasar'
import {onMounted, computed, ref} from 'vue'
import {useI18n} from 'vue-i18n'
import {useAuthStore} from 'stores/auth';
import {useExpenseCategoriesStore} from 'stores/expenseCategories';

const authStore = useAuthStore()
const expenseCategoriesStore = useExpenseCategoriesStore()
const {t} = useI18n()

const category = ref(1)
const data = ref([])

const series = computed(() => [{
	data: data.value.map(x => {
		return {
			x: x.nickname,
			y: x.avg,
		}
	}),
}],)

const chartOptions = {
	chart: {
		type: 'bar',
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
	plotOptions: {
		bar: {
			horizontal: true
		}
	},
	xaxis: {
		type: 'categories'
	},
}

async function fetch() {
	const response = await authStore.request({
		url: 'stats/mealcost/' + category.value + '/',
		method: 'get',
	})

	data.value = response?.data
}

onMounted(() => {
	expenseCategoriesStore.fetch()
	fetch()
})
</script>
