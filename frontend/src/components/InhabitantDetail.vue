<template>
	<NestedCardDialog ref="dialog" width="1000px">
		<template #title>
			<q-icon name="person"/>
			{{ t('new_inhabitant') }}
		</template>
		<InhabitantForm ref="inhabitant_form" v-model="inhabitant" @onSubmit="onSubmit"/>
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

const {t} = useI18n()
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

const inhabitant_form = ref()
const dialog = ref()

async function fetch() {
	const response = await authStore.request({
		url: url,
		method: 'get',
	})

	inhabitant.value = response?.data
}

async function onSubmit() {
	const valid = await inhabitant_form.value.validate()
	if (!valid) return

	await authStore.request({
		url: url,
		method: 'put',
		data: inhabitant.value,
	})

	dialog.value.hide()
}

async function onDelete() {
	await authStore.request({
		url: url,
		method: 'delete',
	})

	dialog.value.hide()
}

onMounted(() => {
	fetch()
})

</script>
