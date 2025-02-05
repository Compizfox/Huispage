<template>
  <div class="text-h6">{{ t('personal_info') }}</div>
  <div class="row q-col-gutter-x-sm">
    <q-input
		v-model="first_name"
		:label="t('first_name')"
		:error="v.first_name.$error"
        class="col-4"
        outlined
        dense
        hide-bottom-space
    />
    <q-input
		v-model="last_name"
		:label="t('last_name')"
		:error="v.last_name.$error"
        class="col-8"
        outlined
        dense
        hide-bottom-space
    />
  </div>
  <q-input
	  v-model="nickname"
	  :label="t('nickname')"
	  :error="v.nickname.$error"
      outlined
      dense
      hide-bottom-space
  />
  <DateInput
      v-model="date_of_birth"
      :label="t('date_of_birth')"
	  :error="v.date_of_birth.$error"
      hide-bottom-space
      dense
  />
</template>

<script setup lang="ts">
import {useI18n} from 'vue-i18n'
import DateInput from 'components/DateInput.vue'
import {required} from '@vuelidate/validators'
import {useVuelidate} from '@vuelidate/core'

const first_name = defineModel<string>('first_name', {required: true})
const last_name = defineModel<string>('last_name', {required: true})
const nickname = defineModel<string>('nickname', {required: true})
const date_of_birth = defineModel<string>('date_of_birth', {required: true})

const validations = {
	first_name: {required},
	last_name: {required},
	nickname: {required},
	date_of_birth: {required}
}

const v = useVuelidate(validations, {first_name, last_name, nickname, date_of_birth}, {$lazy: true, $autoDirty: true})

const {t} = useI18n()

async function validate() {
	return await v.value.$validate()
}

defineExpose({
	validate
})
</script>
