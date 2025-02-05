<template>
  <div class="text-h6">{{ t('login_details') }}</div>

  <q-input
	  v-model="username"
	  :label="t('username')"
	  :error="v.username.$error"
      dense
      outlined
      hide-bottom-space
  />
  <q-input
	  v-model="password"
	  :label="t('password')"
	  :error="v.password.$error"
	  type="password"
      dense
      outlined
      hide-bottom-space
  />
  <q-input
	  v-model="email"
	  :label="t('email_address')"
	  :error="v.email.$error"
	  type="email"
      dense
      outlined
      hide-bottom-space
  />
</template>
<script setup lang="ts">
import {useI18n} from 'vue-i18n'
import {required, requiredIf, email as v_email} from '@vuelidate/validators'
import {useVuelidate} from '@vuelidate/core'

const username = defineModel<string>('username', {required: true})
const password = defineModel<string>('password', {required: true})
const email = defineModel<string>('email', {required: true})

const props = defineProps<{
	passwordRequired: boolean,
}>()

const validations = {
	username: {required},
	password: {requiredIfFoo: requiredIf(props.passwordRequired)},
	email: {required, v_email},
}

const v = useVuelidate(validations, {username, password, email}, {$lazy: true, $autoDirty: true})

const {t} = useI18n()

async function validate() {
	return await v.value.$validate()
}

defineExpose({
	validate
})
</script>
