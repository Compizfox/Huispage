import {defineStore} from 'pinia'
import {api} from 'boot/axios'
import axios, {AxiosRequestConfig, AxiosResponse} from 'axios'
import {useQuasar} from 'quasar'

import type {Inhabitant} from 'src/models/Inhabitant'

const $q = useQuasar()

export const useAuthStore = defineStore('auth', {
	state: () => ({
		returnUrl: null as string | null,
		inhabitant: JSON.parse(localStorage.getItem('inhabitant') || 'null') as Inhabitant | null,
	}),
	actions: {
		async login(username: string, password: string) {
			try {
				const response = await api.post('auth/login', {username, password})
				this.inhabitant = response.data
				localStorage.setItem('inhabitant', JSON.stringify(this.inhabitant))

				// redirect to previous url or default to home page
				this.router.push(this.returnUrl || '/')
			} catch (e) {
				if (axios.isAxiosError(e) && e.response?.status === 401) {
					throw new Error('Wrong credentials')
				} else {
					throw e
				}
			}
		},
		async logout() {
			try {
				await api.get('auth/logout')
			} catch (e) {}
			this.inhabitant = null
			localStorage.removeItem('inhabitant')
			this.router.push({name: 'login'})
		},
		async request(config: AxiosRequestConfig): Promise<AxiosResponse | void> {
			try {
				return await api.request(config)
			} catch (e) {
				if (axios.isAxiosError(e)) {
					if (e.response?.status === 403) {
						await this.logout()
					} else {
						$q.notify({
							type: 'negative',
							message: e.message,
						})
					}
				} else {
					throw e
				}
			}
		}
	}
});

