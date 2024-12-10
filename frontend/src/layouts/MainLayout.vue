<template>
	<q-layout view="hHh Lpr fFf">
		<q-header elevated class="bg-primary text-white" height-hint="98">
			<q-toolbar>
				<q-toolbar-title>
					<q-avatar>
						<img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
					</q-avatar>
					<span class="gt-xs inline">Huispage</span>
				</q-toolbar-title>

				<q-tabs
					inline-label
					:dense="$q.screen.xs"
					outside-arrows
				>
					<q-route-tab
						:to="{ name: 'mealPlanning' }"
						:label="$q.screen.gt.xs ? t('tabs.mealPlanning'): undefined"
						icon="restaurant"
					/>
					<q-route-tab
						:to="{ name: 'expenses' }"
						:label="$q.screen.gt.xs ? t('tabs.expenses') : undefined"
						icon="receipt_long"
					/>
					<q-route-tab
						:to="{ name: 'fridgeAccounting' }"
						:label="$q.screen.gt.xs ? t('tabs.fridgeAccounting') : undefined"
						icon="sports_bar"
					/>
					<q-route-tab
						:to="{ name: 'stats' }"
						:label="$q.screen.gt.xs ? t('tabs.stats') : undefined"
						icon="insights"
					/>
					<q-route-tab
						:to="{ name: 'settings' }"
						:label="$q.screen.gt.xs ? t('tabs.settings'): undefined"
						icon="settings"
						v-if="authStore.inhabitant?.is_superuser"
					/>
				</q-tabs>

				<q-space/>

				<q-btn-dropdown
					flat
					:label="$q.screen.gt.sm ? authStore.inhabitant?.nickname: undefined"
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

<script setup lang="ts">
import {useQuasar} from 'quasar'
import {useI18n} from 'vue-i18n'
import {useAuthStore} from 'stores/auth'

const {t} = useI18n()
const $q = useQuasar()
const authStore = useAuthStore()
</script>

<style lang="scss">
.q-page-container {
	margin-left: auto;
	margin-right: auto;
	width: fit-content;
}

.q-page {
	padding-top: 2rem;
}

.q-tabs {
	max-width: 70%;
}

.q-tab {
	@media (max-width: $breakpoint-xs-max) {
		padding: 0 2px;
	}
}
</style>
