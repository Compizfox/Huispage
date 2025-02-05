<template>
	<div class="text-h6">{{ t('inhabitant_info') }}</div>

	<div class="row q-col-gutter-x-sm">
		<DateInput
			class="col-6"
			v-model="date_entrance"
			:label="t('entrance_date')"
			:error="v.date_entrance.$error"
			hide-bottom-space
			dense
		/>
		<DateInput
			class="col-6"
			v-model="date_leave"
			:label="t('leave_date')"
			hide-bottom-space
			dense
		/>
	</div>

	<q-input
		v-model="start_balance"
		:label="t('start_balance')"
		:error="v.start_balance.$error"
		outlined
		dense
		hide-bottom-space
		type="number"
		prefix="€"
	/>

	<q-checkbox
		v-model="is_superuser"
		label="Superuser"
	/>
</template>
<script setup lang="ts">
import {useI18n} from 'vue-i18n'
import {required, decimal} from '@vuelidate/validators'
import {useVuelidate} from '@vuelidate/core'
import DateInput from 'components/DateInput.vue'

const date_entrance = defineModel<string>('date_entrance', {required: true})
const date_leave = defineModel<string>('date_leave', {required: true})
const start_balance = defineModel<number>('start_balance', {required: true})
const is_superuser = defineModel<boolean>('is_superuser', {required: true})

const validations = {
	date_entrance: {required},
	start_balance: {required, decimal},
}

const v = useVuelidate(validations, {date_entrance, start_balance}, {$lazy: true, $autoDirty: true})

const {t} = useI18n()

async function validate() {
	return await v.value.$validate()
}

defineExpose({
	validate
})
</script>
