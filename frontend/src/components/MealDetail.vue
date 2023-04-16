<template>
	<q-dialog v-model="alert" @before-hide="close">
		<q-card>
			<q-form @submit="onSubmit()">
				<q-card-section class="row items-center bg-primary text-white">
					<div class="text-h6">
						<q-icon name="restaurant"/>
						Kookbeurt {{ mealModel.date }}
					</div>
					<q-space />
					<q-btn icon="close" flat round dense v-close-popup />
				</q-card-section>

				<q-card-section class="q-gutter-md">
					<q-select
						outlined
						emit-value
						map-options
						:options="inhabitantsStore.getInhabitants"
						option-value="id"
						option-label="nickname"
						v-model="mealModel.cook"
						label="Cook"
					/>

					<q-input
						outlined
						v-model="mealModel.description"
						label="Omschrijving"
					/>

					<q-input
						outlined
						v-model="mealModel.ready_at"
						type="time"
						hint="Ready at"
						step="60"
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
					/>
					<q-btn
						flat
						rounded
						icon="save"
						label="OK"
						type="submit"
						color="primary"
						v-close-popup
					/>
				</q-card-actions>
			</q-form>
		</q-card>
	</q-dialog>
</template>

<script setup lang="ts">
import { onMounted, Ref, ref } from 'vue';
import { useRouter, useRoute } from 'vue-router'
import { useInhabitantsStore } from 'stores/inhabitants'
import { useAuthStore } from 'stores/auth'

import type { Meal } from 'src/models/Meal'

const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()
const inhabitantsStore = useInhabitantsStore()

const alert = ref(true)

const mealModel: Ref<Meal> = ref({})
const url = 'meals/' + route.params.id + '/'

function close() {
	router.back()
}

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
