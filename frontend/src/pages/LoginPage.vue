<template>
	<q-layout view="hHh lpR fFf">
		<q-page-container>
			<q-page class="row justify-center items-center" style="background: linear-gradient(#8274C5, #5A4A9F);">
				<div class="column">
					<div class="row">
						<q-card class="shadow-24" style="width:400px;height:540px;">
							<q-card-section class="bg-accent">
								<h2 class="text-white q-my-md">Huispage</h2>
							</q-card-section>
							<q-card-section>
								<q-fab
									color="primary" @click="switchForm"
									icon="add"
									class="absolute"
									style="top: 0; right: 12px; transform: translateY(-50%);"
								></q-fab>
								<q-form class="q-px-sm q-py-md q-gutter-md">
									<q-input
										v-if="register"
										outlined
										v-model="email"
										type="email"
										label="Email address">
										<template v-slot:prepend>
											<q-icon name="email"/>
										</template>
									</q-input>
									<q-input
										outlined
										v-model="username"
										type="username" label="Username">
										<template v-slot:prepend>
											<q-icon name="person"/>
										</template>
									</q-input>
									<q-input
										outlined
										clearable
										type="password"
										v-model="password"
										label="Password">
										<template v-slot:prepend>
											<q-icon name="lock"/>
										</template>
									</q-input>
									<q-input
										v-if="register"
										type="password"
										outlined
										clearable
										v-model="repassword"
										label="Password confirmation">
										<template v-slot:prepend>
											<q-icon name="lock"/>
										</template>
									</q-input>

									<q-btn
										type="submit"
										unelevated
										size="lg"
										color="primary"
										@click="onSubmit"
										:label="btnLabel"
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
import {useAuthStore} from 'stores/auth';
import {useQuasar} from 'quasar'
import {api} from 'boot/axios'

const $q = useQuasar()

const username = ref('')
const password = ref('')
const repassword = ref('')
const email = ref('')
const register = ref(false)
const btnLabel = ref('Login')

function onSubmit() {
	const authStore = useAuthStore();

	authStore.login(username.value, password.value).catch(e => $q.notify({
		type: 'negative',
		message: e.message,
	}))
}

function switchForm() {
	register.value = !register.value
	btnLabel.value = register.value ? 'Register' : 'Login'
}

onMounted(() => {
	api.get('auth/set_csrf_token')
})
</script>
