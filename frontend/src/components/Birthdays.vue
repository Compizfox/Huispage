<template>
	<q-card>
		<q-card-section>
			<div class="text-h5">
				<q-icon name="cake"/>
				{{ t('upcoming_birthdays') }}
			</div>
		</q-card-section>
		<q-card-section>
			<q-list dense class="rounded-borders">
				<template
					v-for="inhabitant in getUpcomingBirthdays()"
					:key="inhabitant.id"
				>
					<q-item
						v-if="inhabitant.date_of_birth"
					>
						<q-item-section>
							{{ inhabitant.nickname }}
						</q-item-section>
						<q-item-section>
							{{ date.formatDate(inhabitant.date_of_birth, 'D MMMM')}}
						</q-item-section>
						<q-item-section>
							{{ date.getDateDiff(new Date(), inhabitant.date_of_birth, 'years') }}
						</q-item-section>
					</q-item>
				</template>

			</q-list>
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
	const today = new Date();
	const birthDate = new Date(dob);

	// Set the birthday to this year
	let nextBirthday = new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate());

	// If the birthday has already passed this year, set it to next year
	if (nextBirthday < today) {
		nextBirthday.setFullYear(today.getFullYear() + 1);
	}

	return nextBirthday;
}

function getUpcomingBirthdays() {
	const dateRange = [new Date(), new Date()]
	dateRange[1].setMonth(dateRange[0].getMonth() + 1);

	return inhabitantsStore.inhabitants
		.map(inhabitant => ({
			...inhabitant,
			nextBirthday: getNextBirthday(inhabitant.date_of_birth)
		}))
		.filter(inhabitant => inhabitant.nextBirthday >= dateRange[0] && inhabitant.nextBirthday <= dateRange[1])
		.sort((a, b) => a.nextBirthday - b.nextBirthday); // Sort by the closest birthday
}
</script>
