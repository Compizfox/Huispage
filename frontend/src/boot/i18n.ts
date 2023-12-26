import {createI18n} from 'vue-i18n'
import messages from 'src/i18n'
import {boot} from 'quasar/wrappers'

export default boot(({app}) => {
	const i18n = createI18n({
		legacy: false,
		locale: 'en',
		fallbackLocale: 'en',
		globalInjection: true,
		messages
	})

	app.use(i18n)
});
