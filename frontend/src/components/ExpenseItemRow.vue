<template>
<q-tr no-hover>
	<q-td>
		<q-input
			borderless
			hide-bottom-space
			v-model="item.name"
			dense
			:error="v.name.$error"
			:readonly="readOnly"
		/>
	</q-td>
	<q-td>
		<q-input
			borderless
			type="number"
			v-model.number="item.cost"
			mask="#.##"
			prefix="€"
			hide-bottom-space
			dense
			:error="v.cost.$error"
			:readonly="readOnly"
		/>
	</q-td>
	<q-td>
		<q-btn
			icon="close"
			dense
			@click="emit('delete')"
			tabindex="-1"
			:hidden="readOnly"
		/>
	</q-td>
</q-tr>
</template>

<script setup lang="ts">
import {minValue, not, numeric, required, sameAs} from '@vuelidate/validators'
import {useVuelidate} from '@vuelidate/core'
import {computed} from 'vue'

export interface ExpenseItem {
	name: string,
	cost: number,
}

const item = defineModel<ExpenseItem>({required: true})

const emit = defineEmits(['delete'])

const props = defineProps<{
	readOnly: boolean
}>()

const validations = computed(() => {
	if (item.value.name != '' || item.value.cost != 0) {
		return {
			name: {required,},
			cost: {
				required,
				numeric,
				minValueValue: minValue(0),
				sameAsRawValue: not(sameAs(0)),
			},
		}
	} else {
		return {
			name: {},
			cost: {},
		}
	}
})

const v = useVuelidate(validations, item, {$lazy: true, $autoDirty: true})

</script>
