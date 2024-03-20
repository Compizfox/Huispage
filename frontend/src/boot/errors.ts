import { boot } from 'quasar/wrappers'
import {Notify} from 'quasar'
import axios from 'axios'

export default boot(({app}) => {
	app.config.errorHandler = function (err) {
		if (axios.isAxiosError(err)) {
			Notify.create({
				type: 'negative',
				message: err.message,
			})
		}
	}
})
