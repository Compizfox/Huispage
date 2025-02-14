<template>
	<q-page padding>
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
			id="mealPlanning"
			wrap-cells
		>
			<template
				v-for="inhabitantSlot in inhabitantHeaderCellSlots" #[inhabitantSlot]="props"
				:key="inhabitantSlot"
			>
				<q-th :props="props">
					{{ props.col.label }}
				</q-th>
			</template>
			<template #body-cell-date="props">
				<q-td :props="props" :class="(isToday(props.row.date))?'bg-secondary':''">
					<q-btn
						flat
						no-caps
						padding="xs"
						:label="$q.screen.gt.sm ? date.formatDate(props.value, 'dd YYYY-MM-DD') : date.formatDate(props.value,
						'dd')"
						@click="onChangeCooking(props.row.date)"
						:disabled="props.row.meal"
						style="white-space: nowrap;"
					>
						<q-tooltip>{{ t('to_cook') }}</q-tooltip>
					</q-btn>
					<q-badge
						v-if="props.row.meal"
						color="accent"
					>
						{{ Object.values(props.row.enrolments).reduce((a, b) => a + b.n, 0) }}
					</q-badge>
				</q-td>
			</template>
			<template v-for="inhabitantSlot in inhabitantBodyCellSlots" #[inhabitantSlot]="props"
								:key="inhabitantSlot">
				<q-td :props="props" :class="(isToday(props.row.date))?'bg-secondary':''">
					<q-checkbox
						:model-value="isEnrolled(props.value.value.n)"
						:disable="props.value.readOnly"
						checked-icon="chair_alt"
						@update:model-value="(value, evt) =>
					onChangeEnrolmentCheckbox(props.rowIndex, props.col.name, props.row.date, value)"
					>
						<q-tooltip
							v-if="props.value.value.updated_at"
						>
							{{ date.formatDate(props.value.value.updated_at, 'YYYY-MM-DD H:mm:ss') }}
						</q-tooltip>
					</q-checkbox>

					<div
						class="row inline cursor-pointer"
						v-if="props.value.value.n > 1 || (props.value.value.n > 0 && !props.value.readOnly)"
					>
						<q-input
							type="number"
							:model-value="getNumGuests(props.value.value.n)"
							@update:model-value="(value, evt) =>
						onChangeNumGuests(props.rowIndex, props.col.name, props.row.date, value)"
							:disable="props.value.readOnly"
							min="0"
							max="99"
							dense
							prefix="+"
						/>
						<q-tooltip>
							{{ t('guests') }}
						</q-tooltip>
					</div>
					<q-btn
						:to="{ name: 'mealDetail', params: { id: props.row.meal.id }}"
						icon="restaurant"
						no-caps
						padding="xs"
						flat
						v-if="props.row.meal?.cook === props.col.name"
					>
						<q-badge
							v-if="!props.row.meal.expense"
							color="warning"
							floating
							rounded
						/>
						<q-badge
							v-if="props.row.meal.expense"
							color="positive"
							floating
							rounded
						/>
						<q-tooltip>{{ props.col.label }} {{ t('cooking') }}</q-tooltip>
					</q-btn>
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
					{{ t('this_week') }}
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

			<template #top-right>
				<q-checkbox
					v-if="authStore.inhabitant?.is_superuser"
					v-model="settingsStore.adminMode"
					:label="t('admin_mode')"
				/>
			</template>
		</q-table>
	</q-page>
</template>

<script setup lang="ts">
import {useInhabitantsStore} from 'stores/inhabitants'
import {useAuthStore} from 'stores/auth'
import {useSettingsStore} from 'stores/settings'
import {computed, Ref, ref} from 'vue'
import {useI18n} from 'vue-i18n'
import {onBeforeRouteUpdate} from 'vue-router'
import {date, useQuasar} from 'quasar'

import type {Day} from 'src/models/Day'

const {t} = useI18n()
const $q = useQuasar()
const inhabitantsStore = useInhabitantsStore()
const authStore = useAuthStore()
const settingsStore = useSettingsStore()

let currentDate = new Date()

const columns = ref()
const loading = ref(true)
const rows: Ref<Array<Day>> = ref([])

const inhabitantBodyCellSlots = computed(() =>
	inhabitantsStore.getCurrentInhabitants.map(inhabitant => 'body-cell-' + inhabitant.id)
)
const inhabitantHeaderCellSlots = computed(() =>
	inhabitantsStore.getCurrentInhabitants.map(inhabitant => 'header-cell-' + inhabitant.id)
)

const pagination = {
	rowsPerPage: 7
}

inhabitantsStore.fetch().then(() => {
	columns.value = [
		{
			name: 'date',
			label: t('date'),
			align: 'right',
			classes: 'q-table--col-auto-width',
			headerClasses: 'q-table--col-auto-width',
			field: (row: any) => row.date,
		},
	].concat(inhabitantsStore.getCurrentInhabitants.map(inhabitant => {
		return {
			name: inhabitant.id,
			label: inhabitant.nickname,
			align: 'left',
			field: (row: any) => {
				return {
					value: row.enrolments[inhabitant.id],
					readOnly: (inhabitant.username !== authStore.inhabitant?.username || isBeforeToday(row.date)) &&
						(!authStore.inhabitant?.is_superuser || !settingsStore.adminMode),
				}
			}
		}
	}))
})
fetch()

// Returns the ISO week of the date.
function getWeek(d: Date) {
	var date = new Date(d.getTime());
	date.setHours(0, 0, 0, 0);
	// Thursday in current week decides the year.
	date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
	// January 4 is always in week 1.
	var week1 = new Date(date.getFullYear(), 0, 4);
	// Adjust to Thursday in week 1 and count number of weeks from date to week1.
	return 1 + Math.round(((date.getTime() - week1.getTime()) / 86400000
		- 3 + (week1.getDay() + 6) % 7) / 7);
}

// Returns the four-digit year corresponding to the ISO week of the date.
function getWeekYear(d: Date) {
	var date = new Date(d.getTime());
	date.setDate(date.getDate() + 3 - (date.getDay() + 6) % 7);
	return date.getFullYear();
}

async function fetch() {
	loading.value = true

	const response = await authStore.request({
		url: 'dailies/' + getWeekYear(currentDate) + '/' + getWeek(currentDate) + '/',
		method: 'get',
	})

	rows.value = response?.data
	loading.value = false
}

function onChangeEnrolmentCheckbox(row_id: number, inhabitant_id: number, date: string, value: boolean) {
	postEnrolments(inhabitant_id, date, value ? 1 : 0)
}

function onChangeNumGuests(row_id: number, inhabitant_id: number, date: string, value: number) {
	postEnrolments(inhabitant_id, date, Number(value) + 1)
}

async function postEnrolments(inhabitant_id: number, date: string, value: number) {
	await authStore.request({
		url: 'enrolments/',
		method: 'post',
		data: {
			inhabitant: inhabitant_id,
			date: date,
			n: value
		}
	})

	$q.notify({
		type: 'positive',
		message: 'Saved.'
	})

	await fetch()
}

async function onChangeCooking(date: string) {
	await authStore.request({
		url: 'meals/',
		method: 'post',
		data: {
			cook: authStore.inhabitant?.id,
			date: date,
			ready_at: '18:00'
		}
	})

	$q.notify({
		type: 'positive',
		message: 'Saved.'
	})

	await fetch()
}

function today() {
	currentDate = new Date
	fetch()
}

function changeWeek(amount: number) {
	currentDate = date.addToDate(currentDate, {days: 7*amount})
	fetch()
}

function isEnrolled(n: number) {
	return n > 0
}

function getNumGuests(n: number) {
	return n - 1
}

function getCurrentDateString(): string {
	return getWeekYear(currentDate) + ' ' + t('week') + ' ' + getWeek(currentDate)
}

function isToday(dateString: string): boolean {
	return date.isSameDate(date.extractDate(dateString, 'YYYY-MM-DD'), Date(), 'day')
}

function isBeforeToday(dateString: string): boolean {
	return date.extractDate(dateString, 'YYYY-MM-DD') < new Date(new Date().toDateString())
}

onBeforeRouteUpdate(() => {
	fetch()
})
</script>

<style lang="scss">
#mealPlanning .q-icon {
	font-size: 30px;
	@media (min-width: $breakpoint-sm-min) {
		font-size: 40px;
	}
}

#mealPlanning th, #mealPlanning .q-table td {
	padding: 4px;
}

#mealPlanning td {
	vertical-align: middle;
}

#mealPlanning input[type="number"] {
	width: 2rem;
}
</style>
