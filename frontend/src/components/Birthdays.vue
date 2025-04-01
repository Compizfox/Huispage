<template>
	<q-card>
		<q-card-section>
			<div class="text-h5">
				<q-icon name="cake"/>
				{{ t('upcoming_birthdays') }}
			</div>
		</q-card-section>
		<q-card-section>
			<q-markup-table dense flat bordered>
				<tbody>
					<template
						v-for="inhabitant in getUpcomingBirthdays()"
						:key="inhabitant.id"
					>
						<tr v-if="inhabitant.date_of_birth">
							<td>{{ date.formatDate(inhabitant.date_of_birth, 'D MMMM') }}</td>
							<td>{{ inhabitant.nickname }}</td>
							<td>{{ date.getDateDiff(new Date(), inhabitant.date_of_birth, 'years') }}</td>
							<td>
								<q-badge
									v-if="date.getDateDiff(inhabitant.nextBirthday, new Date(), 'days') < 7"
								>
									{{ date.getDateDiff(inhabitant.nextBirthday, new Date(), 'days') }}
									{{ t('days') }}
								</q-badge>
							</td>
						</tr>
					</template>
				</tbody>
			</q-markup-table>
		</q-card-section>
	</q-card>
</template>

<script setup lang="ts">
import {useInhabitantsStore} from 'stores/inhabitants'
import {useI18n} from 'vue-i18n'
import {date} from 'quasar'

const inhabitantsStore = useInhabitantsStore()
const {t} = useI18n()

function getNextBirthday(dob: string) {
	const today = new Date()
	const birthDate = new Date(dob)

	// Set the birthday to this year
	let nextBirthday = new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate())

	// If the birthday has already passed this year, set it to next year
	if (nextBirthday < today) {
		nextBirthday.setFullYear(today.getFullYear() + 1)
	}

	return nextBirthday
}

function getUpcomingBirthdays() {
	const n = 5
	return inhabitantsStore.inhabitants
		.map(inhabitant => ({
			...inhabitant,
			nextBirthday: getNextBirthday(inhabitant.date_of_birth)
		}))
		.filter(inhabitant => inhabitant.nextBirthday >= new Date())
		.sort((a, b) => a.nextBirthday - b.nextBirthday) // Sort by the closest birthday
		.slice(0, n)
}
</script>
