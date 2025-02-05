<template>
	<q-form>
		<q-card-section class="q-gutter-y-md">
			<div class="q-gutter-y-md">
				<q-field
					outlined
					dense
					label="id"
					stack-label
					v-if="inhabitant.id"
				>
					<template v-slot:control>
						{{ inhabitant.id }}
					</template>
				</q-field>

				<LoginDetails
					ref="login_details"
					v-model:username="inhabitant.username"
					v-model:password="inhabitant.password"
					v-model:email="inhabitant.email"
					:password-required="passwordRequired"
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

				<InhabitantData
					ref="inhabitant_data"
					v-model:date_entrance="inhabitant.date_entrance"
					v-model:date_leave="inhabitant.date_leave"
					v-model:start_balance="inhabitant.start_balance"
					v-model:is_superuser="inhabitant.is_superuser"
				/>

				<hr>

				<Preferences
					ref="preferences"
				 	v-model:language="inhabitant.language"
					v-model:enrolment_preference="inhabitant.enrolment_preference"
				/>
			</div>
		</q-card-section>
	</q-form>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import type {Inhabitant} from 'src/models/admin/Inhabitant'
import LoginDetails from 'components/InhabitantForm/LoginDetails.vue'
import PersonalInfo from 'components/InhabitantForm/PersonalInfo.vue'
import InhabitantData from 'components/InhabitantForm/InhabitantData.vue'
import Preferences from 'components/InhabitantForm/Preferences.vue'

const props = defineProps<{
	passwordRequired: boolean,
}>()

const login_details = ref()
const personal_info = ref()
const inhabitant_data = ref()
const preferences = ref()

const inhabitant = defineModel<Inhabitant>({required: true})

async function validate() {
	return await login_details.value.validate() &&
	       await personal_info.value.validate() &&
	       await inhabitant_data.value.validate() &&
	       await preferences.value.validate()
}

defineExpose({
	validate
})
</script>

<style lang="scss">
#enrolmentPreference input[type="number"] {
	width: 4rem;
}
</style>
