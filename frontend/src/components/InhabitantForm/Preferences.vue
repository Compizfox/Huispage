<template>
	<div class="text-h6">{{ t('user_preferences') }}</div>

	<q-select
		outlined
		v-model="language"
		:options="languageOptions"
		hide-bottom-space
		dense
		:label="t('language')"
	/>

	<div class="row q-gutter-md" id="enrolmentPreference">
		<span class="col-12"><b>{{ t('enrolment_preferences') }}</b></span>
		<q-input
			v-for="(day, i) in dows"
			:key="i"
			v-model="enrolment_preference[i]"
			:label="day"
			:error="v[i].$error"
			type="number"
			min="0"
			max="99"
			dense
		/>
	</div>
</template>

<script setup lang="ts">
import {useI18n} from 'vue-i18n'
import {required, integer, minValue} from '@vuelidate/validators'
import {useVuelidate} from '@vuelidate/core'

const {t} = useI18n()

const languageOptions = [
	'en',
	'nl',
]

const dows = {
	0: t('monday'),
	1: t('tuesday'),
	2: t('wednesday'),
	3: t('thursday'),
	4: t('friday'),
	5: t('saturday'),
	6: t('sunday'),
}

interface EnrolmentPreference {
	0: number,
	1: number,
	2: number,
	3: number,
	4: number,
	5: number,
	6: number,
}

const language = defineModel<string>('language', {required: true})
const enrolment_preference = defineModel<EnrolmentPreference>('enrolment_preference', {required: true})

const validations = {
	0: {required, integer, minValueValue: minValue(0)},
	1: {required, integer, minValueValue: minValue(0)},
	2: {required, integer, minValueValue: minValue(0)},
	3: {required, integer, minValueValue: minValue(0)},
	4: {required, integer, minValueValue: minValue(0)},
	5: {required, integer, minValueValue: minValue(0)},
	6: {required, integer, minValueValue: minValue(0)},
}

const v = useVuelidate(validations, enrolment_preference, {$lazy: true, $autoDirty: true})

async function validate() {
	return await v.value.$validate()
}

defineExpose({
	validate
})
</script>
