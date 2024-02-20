<template>
	<q-drawer
		v-model="drawer"
		bordered
	>
		<q-scroll-area class="fit">
			<q-tabs
				vertical
				inline-label
			>
				<q-route-tab :to="{ name: 'inhabitants' }" :label="t('inhabitants')" icon="manage_accounts"/>
			</q-tabs>

		</q-scroll-area>
	</q-drawer>
	<router-view/>
</template>

<script setup lang="ts">
import {useI18n} from 'vue-i18n'
import {ref} from 'vue'

const {t} = useI18n()

const drawer = ref(true)
</script>
