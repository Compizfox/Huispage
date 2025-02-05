<template>
	<NestedCardDialog ref="dialog" width="1000px">
		<template #title>
			<q-icon name="person"/>
			{{ t('new_inhabitant') }}
		</template>
		<InhabitantForm
			ref="form"
			v-model="inhabitant"
			:password-required="true"
		/>
		<q-card-actions align="right">
			<q-btn
				flat
				rounded
				icon="save"
				:label="t('to_save')"
				color="primary"
				@click="onSubmit"
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {ref, Ref} from 'vue'
import {date} from 'quasar'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import InhabitantForm from 'components/InhabitantForm/InhabitantForm.vue'
import {useAuthStore} from 'stores/auth';
import {useI18n} from 'vue-i18n'

import type {Inhabitant} from 'src/models/admin/Inhabitant'

const {t} = useI18n()
const authStore = useAuthStore()

const url = 'admin/inhabitants/'

// New empty Inhabitant
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

const form = ref()
const dialog = ref()

async function onSubmit() {
	const valid = await form.value.validate()
	if (!valid) return

	await authStore.request({
		url: url,
		method: 'post',
		data: inhabitant.value,
	})

	dialog.value.hide()
}
</script>
