<template>
	<q-dialog v-model="alert" @before-hide="close">
		<q-card>
			<q-card-section class="row items-center bg-primary text-white">
				<div class="text-h6">Alert</div>
				<q-space/>
				<q-btn icon="close" flat round dense v-close-popup/>
			</q-card-section>

			<q-card-section class="q-pt-none">
				<ExpenseForm></ExpenseForm>
			</q-card-section>

			<q-card-actions align="right">
				<q-btn flat label="OK" color="primary" v-close-popup/>
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>

<script setup lang="ts">
import {onMounted, Ref, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'

import ExpenseForm from 'components/ExpenseForm.vue'
import {useAuthStore} from 'stores/auth'

import type {Expense} from "src/models/Expense";

const router = useRouter()
const route = useRoute()

const authStore = useAuthStore()

const alert = ref(true)
const expenseModel: Ref<Expense> = ref({})

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
