<template>
	<NestedCardDialog ref="dialog" width="1000px">
		<template #title>
			<q-icon name="person"/>
			{{ inhabitant.nickname }}
		</template>
		<InhabitantForm
			ref="form"
			v-model="inhabitant"
			:password-required="false"
		/>
		<q-card-actions align="right">
			<q-btn
				flat
				rounded
				icon="delete"
				:label="t('to_delete')"
				color="negative"
				@click="onDelete"
				v-close-popup
			/>
			<q-btn
				flat
				rounded
				icon="save"
				:label="t('to_save')"
				@click="onSubmit"
				color="primary"
			/>
		</q-card-actions>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {ref, Ref} from 'vue'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import InhabitantForm from 'components/InhabitantForm/InhabitantForm.vue'
import {useAuthStore} from 'stores/auth';
import {useI18n} from 'vue-i18n'
import {useRoute} from 'vue-router'

import type {Inhabitant} from 'src/models/admin/Inhabitant'

const {t} = useI18n()
const route = useRoute()
const authStore = useAuthStore()

const url = 'admin/inhabitants/' + route.params.id + '/'

const inhabitant: Ref<Inhabitant> = ref({enrolment_preference: {}} as Inhabitant)
const form = ref()
const dialog = ref()

fetch()

async function fetch() {
	const response = await authStore.request({
		url: url,
		method: 'get',
	})

	inhabitant.value = response?.data
}

async function onSubmit() {
	const valid = await form.value.validate()
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
</script>
