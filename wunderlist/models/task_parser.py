import re
from workflow import MATCH_ALL, MATCH_ALLCHARS
from wunderlist.util import workflow
from parsedatetime import Calendar
from datetime import date

# Up to 8 words (sheesh!) followed by a colon
_list_title_pattern = r'^((?:\S+ *){1,8}):'

# `every N units` optionally preceded by `repeat`
_recurrence_pattern = r'(?:\brepeat:? )?\bevery (\d*) ?((?:day|week|month|year|d|w|m|y|da|wk|mo|yr)s?)\b'

# Anything following the `due` keyword
_due_pattern = r'(\bdue:?\b)(.*)'

# An asterisk at the end of the phrase
_star_pattern = r'\*$'

# Tabs or multiple consecutive spaces
_whitespace_cleanup_pattern = r'\t|\s{2,}'

# Maps first letter to the API recurrence type
_recurrence_types = {
	'd': 'day',
	'w': 'week',
	'm': 'month',
	'y': 'year'
}

class TaskParser():
	phrase = None
	title = None
	list_id = None
	list_title = None
	due_date = None
	recurrence_type = None
	recurrence_count = None
	assignee_id = None
	starred = False
	completed = False

	_list_phrase = None
	_due_date_phrase = None
	_recurrence_phrase = None
	_starred_phrase = None

	def __init__(self, phrase):
		self.phrase = phrase.strip()
		self._parse()

	def _parse(self):
		phrase = self.phrase
		cal = Calendar()
		wf = workflow()
		lists = wf.stored_data('lists')

		match = re.search(_star_pattern, phrase)
		if match:
			self.starred = True
			self._starred_phrase = match.group()
			phrase = re.sub(_star_pattern, '', phrase)

		match = re.search(_list_title_pattern, phrase)
		if match:
			matching_lists = wf.filter(
				match.group(1),
				lists,
				lambda l:l['title'],
				# Ignore MATCH_ALLCHARS which is expensive and inaccurate
				match_on=MATCH_ALL ^ MATCH_ALLCHARS
			)

			if matching_lists:
				self._list_phrase = match.group()
				phrase = phrase.replace(self._list_phrase, '')
				
				self.list_id = matching_lists[0]['id']
				self.list_title = matching_lists[0]['title']

		if not self.list_title:
			inbox = lists[0]
			self.list_id = inbox['id']
			self.list_title = inbox['title']

		# Parse and remove the recurrence phrase first so that any dates do
		# not interfere with the due date
		match = re.search(_recurrence_pattern, phrase)
		if match:
			self._recurrence_phrase = match.group()
			phrase = phrase.replace(self._recurrence_phrase, '')

			# Look up the recurrence type based on the first letter of the
			# work or abbreviation used in the phrase
			self.recurrence_type = _recurrence_types[match.group(2)[0]]
			self.recurrence_count = int(match.group(1) or 1)

		match = re.search(_due_pattern, phrase)
		if match:
			due_keyword = match.group(1)
			potential_date_phrase = match.group(2)
			dates = cal.nlp(potential_date_phrase)

			if dates:
				# Only remove the first date following `due`
				datetime_info = dates[0]
				# Set due_date if a datetime was found and it is not time only
				if datetime_info[1] != 2:
					self.due_date = datetime_info[0].date()

					# Pull in any words between the `due` keyword and the
					# actual date text					
					due_date_phrase_match = re.search(re.escape(due_keyword) + r'.*?' + re.escape(datetime_info[4]), phrase)

					self._due_date_phrase = due_date_phrase_match.group()
					phrase = phrase.replace(self._due_date_phrase, '')

		# Use nlp to find a date, which can be slightly less featureful
		else:
			dates = cal.nlp(phrase)

			if dates:
				# Only remove the last date for now
				datetime_info = dates[-1]
				if datetime_info[1] != 2:
					self.due_date = datetime_info[0].date()
					phrase = phrase.replace(datetime_info[4], '', 1)

		if self.recurrence_type and not self.due_date:
			self.due_date = date.today()

		# Condense extra whitespace remaining in the task title after parsing
		self.title = re.sub(_whitespace_cleanup_pattern, ' ', phrase).strip()

	def phrase_with(self, list_title=None, due_date=None, recurrence=None, starred=None):
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
		if self.title:
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
