<template>
	<q-page>
		<router-view></router-view>
		<q-table
			:rows="rows"
			:columns="columns"
			:loading="loading"
			:title="getCurrentDateString()"
			row-key="name"
			:pagination="pagination"
			:rows-per-page-options="[]"
			separator="cell"
			dense
		>
			<template
				v-for="inhabitantSlot in inhabitantHeaderCellSlots" #[inhabitantSlot]="props"
				:key="inhabitantSlot"
			>
				<q-th :props="props">
					<q-chip>
						<q-avatar>
							<img src="https://cdn.quasar.dev/img/boy-avatar.png">
						</q-avatar>
						{{ props.col.label }}
					</q-chip>
				</q-th>
			</template>
			<template #body-cell-date="props">
				<q-td :props="props" :class="(isToday(props.row.date))?'bg-secondary':''">
					<q-icon
						name="today"
						v-if="isToday(props.row.date)"
						size="md"
					/>
					<q-btn flat no-caps :label="props.value" @click="onChangeCooking(props.row.date)">
						<q-tooltip>{{ $t('to_cook') }}</q-tooltip>
					</q-btn>
				</q-td>
			</template>
			<template v-for="inhabitantSlot in inhabitantBodyCellSlots" #[inhabitantSlot]="props"
								:key="inhabitantSlot">
				<q-td :props="props" :class="(isToday(props.row.date))?'bg-secondary':''">
					<router-link
						:to="{ name: 'mealDetail', params: { id: props.row.meal.id }}"
						v-if="props.row.meal?.cook === props.col.name"
					>
						<q-icon
							name="restaurant"
							size="xl"
						>
							<q-tooltip>{{ props.col.label }} {{ $t('cooking') }}</q-tooltip>
						</q-icon>
					</router-link>

					<q-btn-dropdown
						split
						:disable-dropdown="props.value.readOnly"
						:ripple="false"
						flat
					>
						<template #label>
							<q-checkbox
								v-model="props.row.enrolments[props.col.name]"
								:disable="props.value.readOnly"
								checked-icon="chair_alt"
								size="xs"
								@update:model-value="(value, evt) => onChangeEnrolmentCheckbox(props.col.name, props.row.date, value)"
							/>
						</template>

					</q-btn-dropdown>
				</q-td>
			</template>

			<template #pagination>
				<q-btn
					icon="chevron_left"
					color="grey-8"
					round
					dense
					flat
					@click="changeWeek(-1)"
				/>

				<q-btn
					dense
					flat
					@click="today"
				>
					{{ $t('this_week') }}
				</q-btn>

				<q-btn
					icon="chevron_right"
					color="grey-8"
					round
					dense
					flat
					@click="changeWeek(1)"
				/>
			</template>
		</q-table>
	</q-page>
</template>

<script setup lang="ts">
import {useInhabitantsStore} from 'stores/inhabitants'
import {useAuthStore} from 'stores/auth'

import {computed, onMounted, ref} from 'vue'
import {useI18n} from 'vue-i18n'
import {onBeforeRouteUpdate} from 'vue-router'
import {date, useQuasar} from 'quasar';

const {t} = useI18n()
const $q = useQuasar()

const inhabitantsStore = useInhabitantsStore();
const authStore = useAuthStore()

let currentDate = new Date()

function getCurrentDateString(): string {
	return date.formatDate(currentDate, 'YYYY') + ' ' + t('week') + ' ' + date.formatDate(currentDate, 'w')
}

function isToday(dateString: string): boolean {
	return date.isSameDate(date.extractDate(dateString, 'YYYY-MM-DD'), Date(), 'day')
}

const columns = ref()
const loading = ref(true)
const rows = ref([])

const inhabitantBodyCellSlots = computed(() =>
	inhabitantsStore.getCurrentInhabitants.map(inhabitant => 'body-cell-' + inhabitant.id)
)
const inhabitantHeaderCellSlots = computed(() =>
	inhabitantsStore.getCurrentInhabitants.map(inhabitant => 'header-cell-' + inhabitant.id)
)

const pagination = {
	rowsPerPage: 7
}

function fetch() {
	authStore.request({
		url: 'dailies/' + date.formatDate(currentDate, 'YYYY') + '/' + date.getWeekOfYear(currentDate) + '/',
		method: 'get',
	}).then(response => {
		rows.value = response?.data
	}).finally(() => {
		loading.value = false
	})
}

function onChangeEnrolmentCheckbox(inhabitant_id: number, date: string, value: boolean) {
	authStore.request({
		url: 'enrolments/',
		method: 'post',
		data: {
			inhabitant: inhabitant_id,
			date: date,
			value: value
		}
	}).then(() => {
		$q.notify({
			type: 'positive',
			message: 'Saved.'
		})
		loading.value = true
		fetch()
	})
}

function onChangeCooking(date: string) {
	authStore.request({
		url: 'meals/',
		method: 'post',
		data: {
			cook: authStore.inhabitant.id,
			date: date,
			ready_at: '18:00'
		}
	}).then(() => {
		$q.notify({
			type: 'positive',
			message: 'Saved.'
		})
		loading.value = true
		fetch()
	}).catch(e => {
		$q.notify({
			type: 'negative',
			message: e.message,
		})
	})
}

function today() {
	currentDate = new Date
	fetch()
}

function changeWeek(amount: number) {
	currentDate = date.addToDate(currentDate, {days: 7*amount})
	loading.value = true
	fetch()
}

onBeforeRouteUpdate(async (to, from) => {
	fetch()
})

onMounted(() => {
	inhabitantsStore.fetch().then(() => {
		columns.value = [
			{
				name: 'date',
				label: t('Date'),
				align: 'right',
				classes: 'q-table--col-auto-width',
				headerClasses: 'q-table--col-auto-width',
				field: (row: any) => row.date,
				format: (val: any) => date.formatDate(val, 'dddd YYYY-MM-DD'),
			},
		].concat(inhabitantsStore.getCurrentInhabitants.map(inhabitant => {
			return {
				name: inhabitant.id,
				label: inhabitant.nickname,
				align: 'right',
				field: (row: any) => {
					return {
						value: row.enrolments[inhabitant.id],
						readOnly: inhabitant.username !== authStore.inhabitant.username && !authStore.inhabitant.is_superuser,
					}
				}
			}
		}))
	})
	fetch()
})

</script>
