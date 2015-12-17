import re
from workflow import MATCH_ALL, MATCH_ALLCHARS
from wunderlist.util import workflow, parsedatetime_calendar
from wunderlist.models.preferences import Preferences
from datetime import date, datetime, time, timedelta
import locale

# Up to 8 words (sheesh!) followed by a colon
_list_title_pattern = r'^((?:[^\s:]+ *){0,8}):'

# `every N units` optionally preceded by `repeat`
_recurrence_pattern = r'(?:\brepeat(?:ing|s)?:? )?(?:\bevery *(\d*) *((?:day|week|month|year|d|w|m|y|da|wk|mo|yr)s?\b)?|(daily|weekly|monthly|yearly|annually))'
_recurrence_by_date_pattern = r'(?:\brepeat:? )?\bevery *((?:\S+ *){0,2})'

_reminder_pattern = r'(\b(?:remind me|reminder|remind|r|alarm)\b:? *)(.*)'

# Anything following the `due` keyword
_due_pattern = r'(\bdue:?\b\s*)(.*)'

_not_due_pattern = r'not? due( date)?'

# An asterisk at the end of the phrase
_star_pattern = r'\*$'

# Tabs or multiple consecutive spaces
_whitespace_cleanup_pattern = r'\t|\s{2,}'

# Maps first letter to the API recurrence type
_recurrence_types = {
	'd': 'day',
	'w': 'week',
	'm': 'month',
	'y': 'year',
	# for "annually"
	'a': 'year'
}

class TaskParser(object):
	phrase = None
	title = None
	list_id = None
	list_title = None
	due_date = None
	recurrence_type = None
	recurrence_count = None
	reminder_date = None
	assignee_id = None
	starred = False
	completed = False

	has_list_prompt = False
	has_due_date_prompt = False
	has_recurrence_prompt = False
	has_reminder_prompt = False

	_list_phrase = None
	_due_date_phrase = None
	_recurrence_phrase = None
	_reminder_phrase = None
	_starred_phrase = None

	def __init__(self, phrase):
		self.phrase = phrase.strip()
		self._parse()

	def _parse(self):
		phrase = self.phrase
		cal = parsedatetime_calendar()
		wf = workflow()
		lists = wf.stored_data('lists')
		prefs = Preferences.current_prefs()
		ignore_due_date = False

		match = re.search(_star_pattern, phrase)
		if match:
			self.starred = True
			self._starred_phrase = match.group()
			phrase = phrase[:match.start()] + phrase[match.end():]

		match = re.search(_not_due_pattern, phrase)
		if match:
			ignore_due_date = True
			phrase = phrase[:match.start()] + phrase[match.end():]

		match = re.search(_list_title_pattern, phrase, re.IGNORECASE)
		if lists and match:
			if match.group(1):
				matching_lists = wf.filter(
					match.group(1),
					lists,
					lambda l:l['title'],
					# Ignore MATCH_ALLCHARS which is expensive and inaccurate
					match_on=MATCH_ALL ^ MATCH_ALLCHARS
				)

				# Take the first match as the desired list
				if matching_lists:
					self.list_id = matching_lists[0]['id']
					self.list_title = matching_lists[0]['title']
			# The list name was empty
			else:
				self.has_list_prompt = True

			if self.list_title or self.has_list_prompt:
				self._list_phrase = match.group()
				phrase = phrase[:match.start()] + phrase[match.end():]

		if not self.list_title:
			if lists:
				inbox = lists[0]
				self.list_id = inbox['id']
				self.list_title = inbox['title']
			else:
				self.list_id = 0
				self.list_title = 'Inbox'

		# Parse and remove the recurrence phrase first so that any dates do
		# not interfere with the due date
		match = re.search(_recurrence_pattern, phrase, re.IGNORECASE)
		if match:
			type_phrase = match.group(2) if match.group(2) else match.group(3)
			if type_phrase:
				# Look up the recurrence type based on the first letter of the
				# work or abbreviation used in the phrase
				self.recurrence_type = _recurrence_types[type_phrase[0].lower()]
				self.recurrence_count = int(match.group(1) or 1)
			else:
				match = re.search(_recurrence_by_date_pattern, phrase, re.IGNORECASE)
				if match:
					recurrence_phrase = match.group()
					dates = cal.nlp(match.group(1), version=2)

					if dates:
						# Only remove the first date following `every`
						datetime_info = dates[0]
						# Set due_date if a datetime was found and it is not time only
						if datetime_info[1].hasDate:
							self.due_date = datetime_info[0].date()
							date_expression = datetime_info[4]

							# FIXME: This logic could be improved to better
							# differentiate between week and year expressions

							# If the date expression is only one word and the next
							# due date is less than one week from now, set a
							# weekly recurrence, e.g. every Tuesday
							if len(date_expression.split(' ')) == 1 and self.due_date < date.today() + timedelta(days=8):
								self.recurrence_count = 1
								self.recurrence_type = 'week'
							# Otherwise expect a multi-word value like a date,
							# e.g. every May 17
							else:
								self.recurrence_count = 1
								self.recurrence_type = 'year'

							self.has_recurrence_prompt = False

							# Pull in any words between the `due` keyword and the
							# actual date text
							date_pattern = re.escape(date_expression)
							date_pattern = r'.*?' + date_pattern

							# Prepare to set the recurrence phrase below
							match = re.search(date_pattern, recurrence_phrase, re.IGNORECASE)

			# This is just the "every" keyword with no date following
			if not self.recurrence_type:
				self.has_recurrence_prompt = True

			self._recurrence_phrase = match.group()
			phrase = phrase.replace(self._recurrence_phrase, '', 1)


		reminder_info = None
		match = re.search(_reminder_pattern, phrase, re.IGNORECASE)
		if match:
			datetimes = cal.nlp(match.group(2), version=2)

			# If there is at least one date immediately following the reminder
			# phrase use it as the reminder date
			if datetimes and datetimes[0][2] == 0:
				# Only remove the first date following the keyword
				reminder_info = datetimes[0]

				self._reminder_phrase = match.group(1) + reminder_info[4]
				phrase = phrase.replace(self._reminder_phrase, '', 1)
			# Otherwise if there is just a reminder phrase, set the reminder
			# to the default time on the date due
			else:
				# There is no text following the reminder phrase, prompt for a reminder
				if not match.group(2):
					self.has_reminder_prompt = True
				self._reminder_phrase = match.group(1)

				# Careful, this might just be the letter "r" so rather than
				# replacing it is better to strip out by index
				phrase = phrase[:match.start(1)] + phrase[match.end(1):]


		due_keyword = None
		potential_date_phrase = None
		if not ignore_due_date:
			match = re.search(_due_pattern, phrase, re.IGNORECASE)
			# Search for the due date only following the `due` keyword
			if match:
				due_keyword = match.group(1)

				if match.group(2):
					potential_date_phrase = match.group(2)
			# Otherwise find a due date anywhere in the phrase
			elif not prefs.explicit_keywords:
				potential_date_phrase = phrase

		if potential_date_phrase:
			dates = cal.nlp(potential_date_phrase, version=2)

			if dates:
				# Only remove the first date following `due`
				datetime_info = dates[0]
				# Set due_date if a datetime was found and it is not time only
				if datetime_info[1].hasDate:
					self.due_date = datetime_info[0].date()

					# Pull in any words between the `due` keyword and the
					# actual date text
					date_pattern = re.escape(datetime_info[4])

					if due_keyword:
						date_pattern = re.escape(due_keyword) + r'.*?' + date_pattern

					due_date_phrase_match = re.search(date_pattern, phrase, re.IGNORECASE)

					if due_date_phrase_match:
						self._due_date_phrase = due_date_phrase_match.group()
						phrase = phrase.replace(self._due_date_phrase, '', 1)

					# If the due date specifies a time, set it as the reminder
					if datetime_info[1].hasTime:
						self.reminder_date = datetime_info[0]
				# Just a time component
				else:
					due_keyword = None
			# No dates in the phrase
			else:
				due_keyword = None

		# The word due was not followed by a date
		if due_keyword and not self._due_date_phrase:
			self.has_due_date_prompt = True
			self._due_date_phrase = match.group(1)

			# Avoid accidentally replacing "due" inside words elsewhere in the
			# string
			phrase = phrase[:match.start(1)] + phrase[match.end(1):]

		if self.recurrence_type and not self.due_date:
			self.due_date = date.today()

		if self._reminder_phrase:
			# If a due date is set, a time-only reminder is relative to that
			# date; otherwise if there is no due date it is relative to today
			reference_date = self.due_date if self.due_date else date.today()

			if reminder_info:
				(dt, datetime_context, _, _, _) = reminder_info

				# Date and time; use as-is
				if datetime_context.hasTime and datetime_context.hasDate:
					self.reminder_date = dt
				# Time only; set the reminder on the due day
				elif datetime_context.hasTime:
					self.reminder_date = datetime.combine(reference_date, dt.time())
				# Date only; set the default reminder time on that day
				elif datetime_context.hasDate:
					self.reminder_date = datetime.combine(dt.date(), prefs.reminder_time)
					
			else:
				self.reminder_date = datetime.combine(reference_date, prefs.reminder_time)
		
		# Condense extra whitespace remaining in the task title after parsing
		self.title = re.sub(_whitespace_cleanup_pattern, ' ', phrase).strip()

	def phrase_with(self, title=None, list_title=None, due_date=None, recurrence=None, reminder_date=None, starred=None):
		components = []

		# Retain the current list
		if list_title is None:
			if self._list_phrase:
				components.append(self._list_phrase)
		# Specifies a list by name
		elif isinstance(list_title, basestring):
			list_title = list_title.replace(':', '')
			components.append(list_title + ':')
		# Triggers selection of a list
		elif list_title:
			components.append(':')
		# Remove the current value
		else:
			pass

		# Add the task text
		if title:
			components.append(title)
		elif self.title:
			components.append(self.title)

		# Retain the current due date
		if due_date is None:
			if self._due_date_phrase:
				components.append(self._due_date_phrase)
		# Specifies a due date phrase
		elif isinstance(due_date, basestring):
			components.append(due_date)
		# Triggers selection of a due date
		elif due_date:
			components.append('due ')
		# Remove the current value
		else:
			pass

		# Retain the current recurrence
		if recurrence is None:
			if self._recurrence_phrase:
				components.append(self._recurrence_phrase)
		# Specifies a recurrence phrase
		elif isinstance(recurrence, basestring):
			components.append(recurrence)
		# Triggers selection of a recurrence
		elif recurrence:
			components.append('every ')
		# Remove the current value
		else:
			pass

		# Retain the current reminder
		if reminder_date is None:
			if self._reminder_phrase:
				components.append(self._reminder_phrase)
		# Specifies a reminder phrase
		elif isinstance(reminder_date, basestring):
			components.append(reminder_date)
		# Triggers selection of a reminder
		elif reminder_date:
			components.append('remind me ')
		# Remove the current value
		else:
			pass

		# Retain the current star status
		if starred is None:
			if self._starred_phrase:
				components.append(self._starred_phrase)
		# Adds a star
		elif starred:
			components.append('*')
		# Removes the star
		else:
			pass

		phrase = ' '.join(components)
		phrase = re.sub(_whitespace_cleanup_pattern, ' ', phrase)

		return phrase