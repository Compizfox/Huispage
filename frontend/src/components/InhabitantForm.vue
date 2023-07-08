<template>
	<q-form>
		<q-card-section>
			<div class="row q-col-gutter-md">
				<div class="col-12 col-md-6">
					<q-card>
						<q-card-section>
							<div class="text-h6">Login details</div>
						</q-card-section>
						<q-card-section>
							<div class="q-gutter-y-md">
								{{ inhabitant.id }}
								<q-input
									dense
									outlined
									v-model="inhabitant.username"
									:label="t('username')"
								/>
								<q-input
									dense
									outlined
									v-model="inhabitant.password"
									type="password"
									:label="t('password')"
								/>
								<q-input
									dense
									outlined
									v-model="inhabitant.email"
									type="email"
									:label="t('email_address')"
								/>
							</div>
						</q-card-section>
					</q-card>
				</div>

				<div class="col-12 col-md-6">
					<q-card>
						<q-card-section>
							<div class="text-h6">Inhabitant info</div>
						</q-card-section>
						<q-card-section>
							<div class="q-gutter-y-md">
								<div class="row q-col-gutter-sm">
									<q-input
										class="col-4"
										outlined
										dense
										v-model="inhabitant.first_name"
										:label="t('first_name')"
									/>
									<q-input
										class="col-8"
										outlined
										dense
										v-model="inhabitant.last_name"
										:label="t('last_name')"
									/>
								</div>

								<q-input
									outlined
									dense
									v-model="inhabitant.nickname"
									:label="t('nickname')"
								/>

								<DateInput
									v-model="inhabitant.date_of_birth"
									:label="t('date_of_birth')"
									dense
								/>

								<div class="row q-col-gutter-sm">
									<DateInput
										class="col-6"
										v-model="inhabitant.date_entrance"
										:label="t('entrance_date')"
										dense
									/>
									<DateInput
										class="col-6"
										v-model="inhabitant.date_leave"
										:label="t('leave_date')"
										dense
									/>
								</div>

								<q-input
									v-model="inhabitant.start_balance"
									outlined
									dense
									:label="t('start_balance')"
									type="number"
									prefix="€"
								/>
							</div>
						</q-card-section>
					</q-card>
				</div>
				<div class="col-12 col-md-6">
					<q-card>
						<q-card-section>
							<div class="text-h6">User preferences</div>
						</q-card-section>
						<q-card-section>
							<div class="q-gutter-y-md">
								<q-select
									outlined
									v-model="inhabitant.language"
									:options="languageOptions"
									dense
									:label="t('language')"
								/>
								<span>
									Enrolment preferences
								</span>
								<div class="row q-gutter-md" id="enrolmentPreference">
									<q-input
										v-for="(day, i) in dows"
										:key="i"
										type="number"
										v-model="inhabitant.enrolment_preference[i]"
										min="0"
										max="99"
										dense
										:label="day"
									/>
								</div>
							</div>
						</q-card-section>
					</q-card>
				</div>
			</div>

		</q-card-section>
	</q-form>
</template>

<script setup lang="ts">
import {computed} from 'vue'
import {useI18n} from 'vue-i18n'
import type {Inhabitant} from 'src/models/admin/Inhabitant'
import DateInput from 'components/DateInput.vue'


const {t} = useI18n()

const languageOptions = [
	'en',
	'nl',
]

const dows = {
	0: 'Monday',
	1: 'Tuesday',
	2: 'Wednesday',
	3: 'Thursday',
	4: 'Friday',
	5: 'Saturday',
	6: 'Sunday',
}

// For component v-model
const props = defineProps<{ modelValue: Inhabitant }>()
const emit = defineEmits(['update:modelValue', 'onSubmit'])

const inhabitant = computed({
	get() {
		return props.modelValue
	},
	set(value) {
		emit('update:modelValue', inhabitant)
	}
})
</script>

<style lang="scss">
#enrolmentPreference input[type="number"] {
	width: 4rem;
}
</style>
