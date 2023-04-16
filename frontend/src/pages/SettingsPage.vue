<template>
	<q-drawer
		v-model="drawer"
		show-if-above
		:width="200"
		:breakpoint="500"
		bordered
	>
		<q-scroll-area class="fit">
			<q-list>
				<q-item clickable>
					<q-item-section avatar>
						<q-icon name="manage_accounts"/>
					</q-item-section>
					<q-item-section>

					</q-item-section>
				</q-item>

			</q-list>
		</q-scroll-area>
	</q-drawer>
	<q-page padding>
		<router-view />
	</q-page>
</template>

<script setup lang="ts">

</script>

<style scoped>

</style>
