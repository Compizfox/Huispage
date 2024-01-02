<template>
	<q-page>
		<router-view></router-view>

		<q-table
			:rows="rows"
			:columns="columns"
			:loading="loading"
			row-key="id"
			:rows-per-page-options="[0]"
			hide-pagination
			:title="t('inhabitants')"
		>
			<template #top-right>
				<router-link
					:to="{ name: 'createInhabitant' }"
				>
					<q-btn color="primary" :label="t('new')"/>
				</router-link>
			</template>

			<template #body-cell-edit="props">
				<q-td :props="props">
					<router-link :to="{ name: 'inhabitantDetail', params: { id: props.row.id }}">
						<q-icon name="edit"/>
					</router-link>
				</q-td>
			</template>
		</q-table>
	</q-page>
</template>

<script setup lang="ts">

import {useI18n} from 'vue-i18n'
import {onMounted, Ref, ref} from 'vue'
import {useAuthStore} from 'stores/auth'

import type {Inhabitant} from 'src/models/admin/Inhabitant'
import {onBeforeRouteUpdate} from 'vue-router'

const {t} = useI18n()

const rows: Ref<Array<Inhabitant>> = ref([])
const loading = ref(true)
const columns = [
	{
		name: 'name',
		label: t('name'),
		field: (row: Inhabitant) => row.first_name + ' ' + row.last_name,
		align: 'left',
	},
	{
		name: 'nickname',
		label: t('nickname'),
		field: (row: Inhabitant) => row.nickname,
		align: 'left',
	},
	{
		name: 'username',
		label: t('username'),
		field: (row: Inhabitant) => row.username,
		align: 'left',
	},
	{
		name: 'dob',
		label: t('date_of_birth'),
		field: (row: Inhabitant) => row.date_of_birth,
		sortable: true,
		align: 'left',
	},
	{
		name: 'date_entrance',
		label: t('entrance_date'),
		field: (row: Inhabitant) => row.date_entrance,
		sortable: true,
		align: 'left',
	},
	{
		name: 'date_leave',
		label: t('leave_date'),
		field: (row: Inhabitant) => row.date_leave,
		sortable: true,
		align: 'left',
	},
	{
		name: 'is_superuser',
		label: t('admin'),
		field: (row: Inhabitant) => row.is_superuser,
		format: (val: boolean) => val ? '\u2611' : '\u2610',
	},
	{
		name: 'edit',
		label: '',
		align: 'center',
	},
]

async function fetch() {
	loading.value = true
	const response = await useAuthStore().request({url: 'admin/inhabitants/', method: 'get'})
	rows.value = response?.data
	loading.value = false
}

onMounted(() => {
	fetch()
})

onBeforeRouteUpdate( () => {
	fetch()
})
</script>
