import {defineStore} from 'pinia'

export const useSettingsStore = defineStore('settings', {
	state: () => ({
		showAllInhabitants: false as boolean,
		adminMode: false as boolean,
	}),
});
