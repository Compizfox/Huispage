<template>
	<q-layout view="hHh Lpr fFf">
		<q-header elevated class="bg-primary text-white" height-hint="98">
			<q-toolbar>
				<q-toolbar-title>
					<q-avatar>
						<img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
					</q-avatar>
					Huispage
				</q-toolbar-title>

				<q-tabs
					inline-label
					outside-arrows
				>
					<q-route-tab :to="{ name: 'mealPlanning' }" :label="t('tabs.mealPlanning')" icon="restaurant"/>
					<q-route-tab :to="{ name: 'expenses' }" :label="t('tabs.expenses')" icon="receipt_long"/>
					<q-route-tab :to="{ name: 'fridgeAccounting' }" :label="t('tabs.fridgeAccounting')" icon="sports_bar"/>
					<q-route-tab :to="{ name: 'stats' }" :label="t('tabs.stats')" icon="insights"/>
					<q-route-tab
						:to="{ name: 'settings' }" :label="t('tabs.settings')"
						icon="settings"
						v-if="authStore.inhabitant?.is_superuser"
					/>
				</q-tabs>

				<q-space/>

				<q-btn-dropdown
					flat
					:label="$q.screen.gt.sm ? authStore.inhabitant?.nickname: ''"
					icon="account_circle"
					dense
					padding="none"
				>
					<q-list>
						<q-item clickable @click="authStore.logout">
							<q-item-section avatar>
								<q-icon color="primary" name="logout"/>
							</q-item-section>
							<q-item-section>Logout</q-item-section>
						</q-item>
					</q-list>
				</q-btn-dropdown>
			</q-toolbar>
		</q-header>

		<q-page-container>
			<router-view/>
		</q-page-container>
	</q-layout>
</template>

<style>
.q-page-container {
	margin-left: auto;
	margin-right: auto;
	width: fit-content;
}

.q-page {
	padding-top: 2rem;
}
</style>

<script setup lang="ts">
import {useAuthStore} from 'stores/auth'
import {useI18n} from 'vue-i18n'

const {t} = useI18n()
const authStore = useAuthStore()
</script>

<style>
.q-tabs {
	max-width: 70%;
}
</style>
