<template>
	<NestedCardDialog>
		<template #title>
			<q-icon name="restaurant"/>
			Kookbeurt {{ mealModel.date }}
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
					v-model="mealModel.cook"
					label="Cook"
					:disable="readOnly"
				/>

				<q-input
					outlined
					v-model="mealModel.description"
					label="Omschrijving"
					:disable="readOnly"
				/>

				<q-input
					outlined
					v-model="mealModel.ready_at"
					type="time"
					hint="Ready at"
					step="60"
					:disable="readOnly"
				/>
			</q-card-section>

			<q-card-actions align="around">
				<q-btn
					flat
					rounded
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
					icon="save"
					label="OK"
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
import {onMounted, Ref, ref} from 'vue'
import {useRoute} from 'vue-router'
import {useInhabitantsStore} from 'stores/inhabitants'
import {useAuthStore} from 'stores/auth'

import type {Meal} from 'src/models/Meal'
import NestedCardDialog from 'components/NestedCardDialog.vue'
import {useSettingsStore} from 'stores/settings'

const route = useRoute()

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()
const settingsStore = useSettingsStore()


const mealModel: Ref<Meal> = ref({
	cook: null,
	participants: [],
	description: '',
	created_at: '',
	updated_at: '',
	date: '',
	ready_at: '',
})
const url = 'meals/' + route.params.id + '/'
const readOnly = ref(mealModel.value.cook !== authStore.inhabitant?.id &&
	(!authStore.inhabitant?.is_superuser || !settingsStore.adminMode))

function fetch() {
	authStore.request({
		url: url,
		method: 'get',
	}).then(response => {
		mealModel.value = response?.data
	})
}

function onSubmit() {
	authStore.request({
		url: url,
		method: 'put',
		data: mealModel.value,
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

<style scoped>

</style>
