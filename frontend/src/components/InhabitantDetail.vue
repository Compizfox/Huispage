<template>
	<NestedCardDialog width="1000px">
		<template #title>
			<q-icon name="person"/>
			{{ t('new_inhabitant') }}
		</template>
		<InhabitantForm v-model="inhabitant" @onSubmit="onSubmit"/>
		<q-card-actions align="right">
			<q-btn
				flat
				rounded
				icon="delete"
				:label="t('delete')"
				color="negative"
				@click="onDelete"
				v-close-popup
			/>
			<q-btn
				flat
				rounded
				icon="save"
				label="OK"
				@click="onSubmit"
				color="primary"
				v-close-popup
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {onMounted, ref, Ref} from 'vue'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import InhabitantForm from 'components/InhabitantForm.vue'
import {useAuthStore} from 'stores/auth';
import {useI18n} from 'vue-i18n'
import {useRoute} from 'vue-router'

import type {Inhabitant} from 'src/models/admin/Inhabitant'
import {useQuasar} from 'quasar'

const {t} = useI18n()
const $q = useQuasar()
const route = useRoute()
const authStore = useAuthStore()

const url = 'admin/inhabitants/' + route.params.id + '/'

// New empty Expense
const inhabitant: Ref<Inhabitant> = ref({
	id: null,
	username: '',
	password: '',
	email: '',
	first_name: '',
	last_name: '',
	nickname: '',
	language: '',
	date_of_birth: '',
	date_entrance: '',
	date_leave: '',
	is_superuser: false,
	enrolment_preference: {
		0: 1,
		1: 1,
		2: 1,
		3: 1,
		4: 1,
		5: 0,
		6: 0,
	},
	start_balance: 0,
})

function fetch() {
	authStore.request({
		url: url,
		method: 'get',
	}).then(response => {
		inhabitant.value = response?.data
	})
}

function onSubmit() {
	authStore.request({
		url: url,
		method: 'put',
		data: inhabitant.value,
	}).catch(e => {
		$q.notify({
			type: 'negative',
			message: e.message,
		})
	})
}

function onDelete() {
	authStore.request({
		url: url,
		method: 'delete',
	})
}

onMounted(() => {
	fetch()
})

</script>
