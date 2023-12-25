<template>
	<q-layout view="hHh lpR fFf">
		<q-page-container>
			<q-page class="row justify-center items-center" style="background: linear-gradient(#8274C5, #5A4A9F);">
				<div class="column">
					<div class="row">
						<q-card class="shadow-24">
							<q-card-section class="bg-accent">
								<h2 class="text-white q-my-md">Huispage</h2>
							</q-card-section>
							<q-card-section>
								<q-form
									class="q-px-sm q-py-md q-gutter-md"
									@submit.prevent="onSubmit"
								>
									<q-input
										outlined
										v-model="username"
										type="text"
										label="Username">
										<template #prepend>
											<q-icon name="person"/>
										</template>
									</q-input>
									<q-input
										outlined
										clearable
										type="password"
										v-model="password"
										label="Password">
										<template #prepend>
											<q-icon name="lock"/>
										</template>
									</q-input>
									<q-btn
										type="submit"
										unelevated
										size="lg"
										color="primary"
										label="Login"
									/>
								</q-form>
							</q-card-section>
						</q-card>
					</div>
				</div>
			</q-page>
		</q-page-container>
	</q-layout>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {useAuthStore} from 'stores/auth'
import {useQuasar} from 'quasar'
import {api} from 'boot/axios'

const $q = useQuasar()
const authStore = useAuthStore();

const username = ref('')
const password = ref('')

function onSubmit() {
	authStore.login(username.value, password.value).catch(e => $q.notify({
		type: 'negative',
		message: e.message,
	}))
}

onMounted(() => {
	api.get('auth/set_csrf_token')
})
</script>
