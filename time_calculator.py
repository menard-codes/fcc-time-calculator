def extractor(start, duration):
	broken_duration = duration.split(':')
	splitted_duration = [int(x) for x in broken_duration]

	broken_start = start.split(' ')
	splitted_start = []
	for x in broken_start:
		if ':' in x:
			hour_minute_split = x.split(':')
			for x in hour_minute_split:
				splitted_start.append(int(x))
		else:
			splitted_start.append(x)
	return splitted_start, splitted_duration


def time_addition(start, duration):

	splitted_start, splitted_duration = extractor(start, duration)

	result = {'hour': 0, 'minute': 0}
	plus_one_hour = False

	minute_sum = splitted_start[1] + splitted_duration[1]
	if minute_sum < 60:
		if len(str(minute_sum)) == 1:
			result['minute'] = f'0{minute_sum}'
		else:
			result['minute'] = minute_sum
	elif minute_sum >= 60:
		minute_final = minute_sum - 60
		plus_one_hour = True
		if len(str(minute_final)) == 1:
			result['minute'] = f'0{minute_final}'
		else:
			result['minute'] = minute_final

	hour_sum = splitted_start[0] + splitted_duration[0]
	if plus_one_hour:
		result['hour'] = hour_sum + 1
	else:
		result['hour'] = hour_sum

	result['period'] = splitted_start[2]

	return result


def time_handler(time_addition, day, days_list, days_dictionary):

	if time_addition['period'] == 'AM':
		hour_period = time_addition['hour'] // 12
		hour_result = time_addition['hour'] % 12
	elif time_addition['period'] == 'PM':
		hour_period = (12 + time_addition['hour']) // 12
		hour_result = (12 + time_addition['hour']) % 12

	def whatPeriod():
		if hour_period % 2 == 0:
			return 'AM'
		elif hour_period % 2 == 1:
			return 'PM'

	def hour_final():
		if hour_result == 0:
			return 12
		elif hour_result > 0:
			return hour_result

	def how_long():
		if hour_period <= 1:	# same day
			return day, ''
		elif 1 < hour_period < 4:	# the next day
			if type(day) is str:
				next_day_index = (days_dictionary[day.title()]) // 7
				end_day = days_list[next_day_index]
				return end_day, ' (next day)'
			else:
				return day, ' (next day)'
		elif hour_period >= 4:
			n_days_later = (time_addition['hour'] // 24) + 1
			if type(day) is str:
				n_days_later_index = ((days_dictionary[day.title()] + n_days_later) // 7) - 2
				end_day = days_list[n_days_later_index]
				return end_day, f' ({n_days_later} days later)'
			else:
				return day, f' ({n_days_later} days later)'

	return whatPeriod(), hour_final(), how_long()

def add_time(start, duration, day=None):

	time_add = time_addition(start, duration)
	days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
	days_dictionary = {day: index for index, day in enumerate(days_list)}

	whatPeriod, hour_final, how_long = time_handler(time_add, day, days_list, days_dictionary)
	end_day, days_later = how_long
	if day == None:
		return f'{hour_final}:{time_add["minute"]} {whatPeriod}{days_later}'
	elif type(day) is str:
		return f'{hour_final}:{time_add["minute"]} {whatPeriod}, {end_day}{days_later}'