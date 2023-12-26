<template>
  <router-view />
</template>

<script setup lang="ts">
import {useAuthStore} from 'stores/auth'
import {useI18n} from 'vue-i18n'

const authStore = useAuthStore()
const {locale} = useI18n()

if (authStore.inhabitant) {
	locale.value = authStore.inhabitant.language
}
</script>
