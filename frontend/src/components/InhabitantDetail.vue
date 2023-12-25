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

const inhabitant: Ref<Inhabitant> = ref({} as Inhabitant)
const inhabitant_form = ref()
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
</script>
