import {defineStore} from 'pinia'
import {useAuthStore} from 'stores/auth'

interface ServerSettings {
	publicly_editable_debitors: boolean,
}

export const useSettingsStore = defineStore('settings', {
	state: () => ({
		server: {} as ServerSettings,
		showAllInhabitants: false as boolean,
		adminMode: false as boolean,
	}),

	actions: {
		async fetch() {
			const response = await useAuthStore().request({url: 'settings/', method: 'get'})
			this.server = response?.data
		}
	}
});
