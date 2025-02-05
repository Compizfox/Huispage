<template>
	<q-input
		outlined
		v-model="model"
		:label="label"
		:error="error"
		mask="####-##-##"
		hide-bottom-space
	>
		<template #append>
			<q-icon name="event" class="cursor-pointer">
				<q-popup-proxy ref="datepickerProxy">
					<q-date
						v-model="model"
						@update:model-value="$refs.datepickerProxy.hide()"
						minimal
						today-btn
					/>
				</q-popup-proxy>
			</q-icon>
		</template>
	</q-input>
</template>

<script setup lang="ts">
const model = defineModel<string>({required: true})
defineProps<{
	label: string,
	error?: boolean,
}>()
</script>
