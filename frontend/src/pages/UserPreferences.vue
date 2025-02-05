<template>
	<q-page padding>
		<q-card>
			<q-card-section>
				<div class="text-h4">{{ t('user_preferences')}}</div>
			</q-card-section>
			<q-form>
				<q-card-section class="q-gutter-y-md">
					<LoginDetails
						ref="login_details"
						v-model:username="inhabitant.username"
						v-model:password="inhabitant.password"
						v-model:email="inhabitant.email"
						:password-required="false"
					/>

					<hr>

					<PersonalInfo
						ref="personal_info"
						v-model:first_name="inhabitant.first_name"
						v-model:last_name="inhabitant.last_name"
						v-model:nickname="inhabitant.nickname"
						v-model:date_of_birth="inhabitant.date_of_birth"
					/>

					<hr>

					<Preferences
						ref="preferences"
						v-model:language="inhabitant.language"
						v-model:enrolment_preference="inhabitant.enrolment_preference"
					/>
				</q-card-section>
				<q-card-actions align="right">
					<q-btn
						flat
						rounded
						icon="save"
						:label="t('to_save')"
						@click="onSubmit"
						color="primary"
					/>
				</q-card-actions>
			</q-form>
		</q-card>
	</q-page>
</template>

<script setup lang="ts">
import {useI18n} from 'vue-i18n'
import {ref, Ref} from 'vue'
import {useQuasar} from 'quasar'
import {useAuthStore} from 'stores/auth'
import type {Inhabitant} from 'src/models/admin/Inhabitant'
import LoginDetails from 'components/InhabitantForm/LoginDetails.vue'
import PersonalInfo from 'components/InhabitantForm/PersonalInfo.vue'
import Preferences from 'components/InhabitantForm/Preferences.vue'

const inhabitant: Ref<Inhabitant> = ref({} as Inhabitant)

const {t, locale} = useI18n({useScope: 'global'})
const $q = useQuasar()
const authStore = useAuthStore()

const url = 'admin/inhabitants/' + authStore.inhabitant!.id + '/'

const login_details = ref()
const personal_info = ref()
const preferences = ref()

fetch()

async function fetch() {
	const response = await authStore.request({
		url: url,
		method: 'get',
	})

	inhabitant.value = response?.data
}

async function onSubmit() {
	const valid = await login_details.value.validate() &&
	              await personal_info.value.validate() &&
	              await preferences.value.validate()
	if (!valid) return

	await authStore.request({
		url: url,
		method: 'put',
		data: inhabitant.value,
	})

	$q.notify({
		type: 'positive',
		message: 'Saved.'
	})

	await fetch()

	await authStore.refresh()
	locale.value = authStore.inhabitant!.language
}
</script>


<style lang="scss">
#enrolmentPreference input[type="number"] {
	width: 4rem;
}
</style>
