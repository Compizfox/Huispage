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
				icon="save"
				label="OK"
				color="primary"
				@click="onSubmit"
				v-close-popup
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {ref, Ref} from 'vue'
import {date, useQuasar} from 'quasar'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import InhabitantForm from 'components/InhabitantForm.vue'
import {useAuthStore} from 'stores/auth';
import {useI18n} from 'vue-i18n'

import type {Inhabitant} from 'src/models/admin/Inhabitant'

const {t} = useI18n()
const $q = useQuasar()
const authStore = useAuthStore()

const url = 'admin/inhabitants/'

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
	date_entrance: date.formatDate(Date.now(), 'YYYY-MM-DD'),
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

function onSubmit() {
	authStore.request({
		url: url,
		method: 'post',
		data: inhabitant.value,
	}).catch(e => {
		$q.notify({
			type: 'negative',
			message: e.message,
		})
	})
}
</script>
