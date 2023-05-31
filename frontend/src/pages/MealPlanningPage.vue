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
		>
			<template
				v-for="inhabitantSlot in inhabitantHeaderCellSlots" #[inhabitantSlot]="props"
				:key="inhabitantSlot"
			>
				<q-th :props="props">
					<q-chip :dense="$q.screen.lt.sm">
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
					/>
					<q-btn
						flat
						no-caps
						padding="xs"
						:label="$q.screen.gt.sm ? date.formatDate(props.value, 'dddd YYYY-MM-DD') : date.formatDate(props.value,
						'dd')"
						@click="onChangeCooking(props.row.date)"
						:disabled="props.row.meal"
					>
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
						>
							<q-tooltip>{{ props.col.label }} {{ $t('cooking') }}</q-tooltip>
						</q-icon>
					</router-link>
					<q-checkbox
						:model-value="isEnrolled(props.row.enrolments[props.col.name])"
						:disable="props.value.readOnly"
						checked-icon="chair_alt"
						@update:model-value="(value, evt) =>
						onChangeEnrolmentCheckbox(props.rowIndex, props.col.name, props.row.date, value)"
					/>
					<div class="row inline cursor-pointer">
						<q-input
							type="number"
							v-if="props.row.enrolments[props.col.name] > 0"
							:model-value="getNumGuests(props.row.enrolments[props.col.name])"
							@update:model-value="(value, evt) =>
						onChangeNumGuests(props.rowIndex, props.col.name, props.row.date, value)"
							:disable="props.value.readOnly"
							min="0"
							max="99"
							dense
						/>
						<q-tooltip>
							Guests
						</q-tooltip>
					</div>

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

import {computed, onMounted, Ref, ref} from 'vue'
import {useI18n} from 'vue-i18n'
import {onBeforeRouteUpdate} from 'vue-router'
import {date, useQuasar} from 'quasar'

import type {Day} from 'src/models/Day'

const {t} = useI18n()
const $q = useQuasar()

const inhabitantsStore = useInhabitantsStore()
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

function onChangeEnrolmentCheckbox(row_id: number, inhabitant_id: number, date: string, value: boolean) {
	let n = value ? 1 : 0
	rows.value[row_id].enrolments[inhabitant_id] = n

	postEnrolments(inhabitant_id, date, n)
}

function onChangeNumGuests(row_id: number, inhabitant_id: number, date: string, value: number) {
	let n = Number(value) + 1
	rows.value[row_id].enrolments[inhabitant_id] = n

	postEnrolments(inhabitant_id, date, n)
}

function postEnrolments(inhabitant_id: number, date: string, value: number) {
	authStore.request({
		url: 'enrolments/',
		method: 'post',
		data: {
			inhabitant: inhabitant_id,
			date: date,
			n: value
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
			cook: authStore.inhabitant?.id,
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

function isEnrolled(n: number) {
	return n > 0
}

function getNumGuests(n: number) {
	return n - 1
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
			},
		].concat(inhabitantsStore.getCurrentInhabitants.map(inhabitant => {
			return {
				name: inhabitant.id,
				label: inhabitant.nickname,
				align: 'right',
				field: (row: any) => {
					return {
						value: row.enrolments[inhabitant.id],
						readOnly: inhabitant.username !== authStore.inhabitant?.username &&
							!authStore.inhabitant?.is_superuser,
					}
				}
			}
		}))
	})
	fetch()
})

</script>

<style lang="scss">
.q-table .q-icon {
	font-size: 30px;
	@media (min-width: $breakpoint-sm-min) {
		font-size: 40px;
	}
}

.q-table th, .q-table td {
	padding: 4px 8px;
	@media (max-width: $breakpoint-sm-min) {
		padding: 4px 4px;
	}
}

.q-table input[type="number"] {
	width: 2rem;
}
</style>
