<template>
	<q-input
		outlined
		:model-value="modelValue"
		@update:modelValue="value => $emit('update:modelValue', value)"
		:label="label"
		:error="error"
		mask="####-##-##"
		hide-bottom-space
	>
		<template #append>
			<q-icon name="event" class="cursor-pointer">
				<q-popup-proxy ref="datepickerProxy">
					<q-date
						:model-value="modelValue"
						@update:modelValue="value => $emit('update:modelValue', value)"
						minimal
						@update:model-value="$refs.datepickerProxy.hide()"
						today-btn
					/>
				</q-popup-proxy>
			</q-icon>
		</template>
	</q-input>
</template>

<script setup lang="ts">
defineProps<{
	modelValue: string,
	label: string,
	error: boolean,
}>()
defineEmits(['update:modelValue'])
</script>
