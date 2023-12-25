<template>
	<NestedCardDialog>
		<template #title>
			<q-icon name="restaurant"/>
			{{ t('meal') }} {{ meal.date }}
		</template>

		<q-form @submit="onSubmit()">
			<q-card-section class="q-gutter-md">
				<q-select
					outlined
					emit-value
					map-options
					:options="inhabitantsStore.getCurrentInhabitants"
					option-value="id"
					option-label="nickname"
					v-model="meal.cook"
					:label="t('cook')"
					:disable="! (authStore.inhabitant?.is_superuser && settingsStore.adminMode)"
				/>

				<q-input
					outlined
					v-model="meal.description"
					:label="t('description')"
					:disable="readOnly"
				/>

				<q-input
					outlined
					v-model="meal.ready_at"
					type="time"
					:hint="t('ready_at')"
					step="60"
					:disable="readOnly"
				/>
			</q-card-section>

			<q-card-actions align="around">
				<q-btn
					flat
					rounded
					no-caps
					icon="delete"
					label="Delete"
					color="negative"
					@click="onDelete"
					v-close-popup
					v-if="!readOnly"
				/>
				<q-btn
					flat
					rounded
					no-caps
					icon="receipt"
					:label="t('save_and_create_expense')"
					@click="onSaveAndCreateExpense"
					v-if="meal.expense == null"
				/>
				<q-btn
					flat
					rounded
					no-caps
					icon="receipt"
					:label="t('save_and_edit_expense')"
					@click="onSaveAndEditExpense"
					v-else
				/>
				<q-btn
					flat
					rounded
					no-caps
					icon="save"
					:label="t('save')"
					type="submit"
					color="primary"
					v-close-popup
					v-if="!readOnly"
				/>
			</q-card-actions>
		</q-form>
	</NestedCardDialog>
</template>

<script setup lang="ts">
import {computed, Ref, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useAuthStore} from 'stores/auth'

import type {Meal} from 'src/models/Meal'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import {useSettingsStore} from 'stores/settings'
import {useI18n} from 'vue-i18n'

const route = useRoute()
const router = useRouter()

const {t} = useI18n()
const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const settingsStore = useSettingsStore()

const meal: Ref<Meal> = ref({} as Meal)
const url = 'meals/' + route.params.id + '/'
const readOnly = computed(() => meal.value?.cook !== authStore.inhabitant?.id &&
	(!authStore.inhabitant?.is_superuser || !settingsStore.adminMode))

fetch()

async function fetch() {
	const response = await authStore.request({
		url: url,
		method: 'get',
	})

	meal.value = response?.data
}

async function onSubmit() {
	await authStore.request({
		url: url,
		method: 'put',
		data: meal.value,
	})
}

function onDelete() {
	authStore.request({
		url: url,
		method: 'delete',
	})
}

async function onSaveAndCreateExpense() {
	await onSubmit()
	await router.push({name: 'createExpense', query: {meal_id: route.params.id}})
}

async function onSaveAndEditExpense() {
	await onSubmit()
	await router.push({name: 'expenseDetail', params: {id: meal.value.expense}})
}
</script>
