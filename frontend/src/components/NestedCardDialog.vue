<template>
	<q-dialog v-model="alert" @before-hide="close">
		<q-card>
			<q-card-section class="row items-center bg-primary text-white">
				<div class="text-h6">
					<slot name="title"></slot>
				</div>
				<q-space/>
				<q-btn icon="close" flat round dense v-close-popup/>
			</q-card-section>
			<slot></slot>
		</q-card>
	</q-dialog>
</template>

<script setup lang="ts">
import {ref} from 'vue';
import {useRouter} from 'vue-router';

const router = useRouter()
const alert = ref(true)

function close() {
	router.back()
}
</script>

<style scoped>

</style>
