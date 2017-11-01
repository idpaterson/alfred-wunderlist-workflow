# encoding: utf-8

from wunderlist.models.task_parser import TaskParser
import pytest
import re
import locale
from datetime import date, datetime, time, timedelta

_inbox = 'Inbox'
_single_word_list = 'Finances'
_multi_word_list = 'Shopping List'
_diacritic_list = u'Jardinería'
_diacritic_list_insensitive = 'Jardineria'

_lists = [
	_inbox,
	_single_word_list,
	_multi_word_list,
	_diacritic_list
]

_default_reminder_time = time(9, 0, 0)
_default_reminder_today_offset = time(1, 0, 0)
_noon = time(12, 0, 0)
_12_13_14 = date(2014, 12, 13)
_today = date.today()
_tomorrow = _today + timedelta(days=1)
_next_week = _today + timedelta(days=7)
_monday = _today + timedelta(days=7 - _today.weekday())
due_date_formats = {
	'12/13/14': _12_13_14,
	'12/13/2014': _12_13_14,
	'Dec 13, 2014': _12_13_14,
	'December 13, 2014': _12_13_14,
	'Dec 13th 2014': _12_13_14,
	'tomorrow': _tomorrow,
	'1d': _tomorrow,
	'next week': _next_week,
	'Monday': _monday,
	'1w': _next_week,
	'in 1 week': _next_week,
	'in 7d': _next_week
}

recurrence_types = {
	'year': 'year',
	'yr': 'year',
	'y': 'year',
	'month': 'month',
	'mo': 'month',
	'm': 'month',
	'week': 'week',
	'wk': 'week',
	'w': 'week',
	'day': 'day',
	'da': 'day',
	'd': 'day'
}

single_recurrence_types = {
	'yearly': 'year',
	'annually': 'year',
	'monthly': 'month',
	'weekly': 'week',
	'daily': 'day'
}

@pytest.fixture
def mock_lists(mocker):
	"""
	Causes stored_data to return the lists specified for this test suite
	"""
	lists = map(lambda (i, title): { 'title': title, 'id': i }, enumerate(_lists))
	mocker.patch('workflow.Workflow.stored_data', new=lambda *arg: lists)

@pytest.fixture
def mock_lists_empty(mocker):
	"""
	Causes stored_data to return an empty array for lists
	"""
	lists = []
	mocker.patch('workflow.Workflow.stored_data', new=lambda *arg: lists)

@pytest.fixture(autouse=True)
def mock_default_reminder_time(mocker):
	"""
	Returns the default reminder time specified above rather than the user's
	preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.reminder_time', new=_default_reminder_time)

@pytest.fixture(autouse=True)
def mock_default_reminder_today_offset(mocker):
	"""
	Use default 1 hour time offset
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.reminder_today_offset', new=_default_reminder_today_offset)

@pytest.fixture()
def mock_2_hour_reminder_today_offset(mocker):
	"""
	Use 2 hours rather than the default 1 hour time offset
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.reminder_today_offset', new=time(2, 0, 0))

@pytest.fixture()
def mock_disabled_reminder_today_offset(mocker):
	"""
	Use None to disable the offset and always use the default reminder time
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.reminder_today_offset', new=None)

@pytest.fixture(autouse=True)
def mock_default_explicit_keywords(mocker):
	"""
	Returns False for explicit_keywords rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.explicit_keywords', new=False)

@pytest.fixture()
def mock_disabled_explicit_keywords(mocker):
	"""
	Returns True for explicit_keywords rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.explicit_keywords', new=True)

@pytest.fixture(autouse=True)
def mock_disabled_automatic_reminders(mocker):
	"""
	Returns False for automatic_reminders rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.automatic_reminders', new=False)

@pytest.fixture()
def mock_enabled_automatic_reminders(mocker):
	"""
	Returns True for automatic_reminders rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.automatic_reminders', new=True)

@pytest.fixture(autouse=True)
def mock_default_list_inbox(mocker):
	"""
	Returns None for default_list_id rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.default_list_id', new=None)

@pytest.fixture()
def mock_default_list_single_word_list(mocker):
	"""
	Returns 1 for default_list_id rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.default_list_id', new=1)

@pytest.fixture()
def mock_default_list_invalid_list(mocker):
	"""
	Returns 8 for default_list_id rather than the user's preference
	"""
	mocker.patch('wunderlist.models.preferences.Preferences.default_list_id', new=8)

@pytest.fixture(autouse=True)
def set_locale():
	"""
	Ensures an en-US locale
	"""
	locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def initials(phrase):
	"""
	Return a string composed of the first letter of each word in the phrase
	"""
	return re.sub(r'(?:^| +)(\S)\S*', r'\1', phrase)

def assert_task(task, phrase=None, title=None, list_id=None, list_title=None, due_date=None, recurrence_type=None, recurrence_count=None, reminder_date=None, assignee_id=None, starred=False, completed=False, has_list_prompt=False, has_due_date_prompt=False, has_recurrence_prompt=False, has_reminder_prompt=False, has_hashtag_prompt=False, note=None):
	assert task.phrase == phrase
	assert task.title == title

	# These will default to the Inbox list, do not assert None
	if list_id:
		assert task.list_id == list_id
	if list_title:
		assert task.list_title == list_title

	assert task.due_date == due_date
	assert task.recurrence_type == recurrence_type
	assert task.recurrence_count == recurrence_count
	assert task.reminder_date == reminder_date
	assert task.assignee_id == assignee_id
	assert task.starred == starred
	assert task.completed == completed
	assert task.has_list_prompt == has_list_prompt
	assert task.has_due_date_prompt == has_due_date_prompt
	assert task.has_recurrence_prompt == has_recurrence_prompt
	assert task.has_reminder_prompt == has_reminder_prompt
	assert task.has_hashtag_prompt == has_hashtag_prompt
	assert task.note == note

#
# Basics
#

class TestBasics():

	def test_blank_phrase(self):
		phrase = ''
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=phrase)

	def test_title(self):
		title = 'a sample task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_phrase_is_trimmed(self):
		title = 'a sample task'
		phrase = title
		task = TaskParser(' %s ' % phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_inbox_is_default(self):
		target_list = _inbox
		title = 'a sample task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	@pytest.mark.usefixtures("mock_default_list_single_word_list", "mock_lists")
	def test_default_list_preference_is_default(self):
		target_list = _single_word_list
		title = 'a sample task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	@pytest.mark.usefixtures("mock_default_list_invalid_list", "mock_lists")
	def test_inbox_is_default_for_invalid_list_preference(self):
		target_list = _inbox
		title = 'a sample task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	@pytest.mark.usefixtures("mock_lists_empty")
	def test_inbox_is_default_before_syncing_lists(self):
		target_list = _inbox
		title = 'a sample task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

#
# Combining reminder dates
#

class TestReminderDateCombine():

	def test_date_and_time(self):
		date_component = _12_13_14
		time_component = _noon
		reminder_date = TaskParser.reminder_date_combine(date_component, time_component)

		assert reminder_date == datetime.combine(date_component, time_component)

	def test_date_and_time_as_datetimes(self):
		date_component = datetime.combine(_12_13_14, _default_reminder_time)
		time_component = datetime.combine(_today, _noon)
		reminder_date = TaskParser.reminder_date_combine(date_component, time_component)

		assert reminder_date == datetime.combine(date_component.date(), time_component.time())

	def test_default_time_not_today(self):
		date_component = _tomorrow
		reminder_date = TaskParser.reminder_date_combine(date_component)

		assert reminder_date == datetime.combine(date_component, _default_reminder_time)

	def test_default_time_today(self):
		date_component = _today
		now = datetime.now()
		reminder_date = TaskParser.reminder_date_combine(date_component)

		assert reminder_date.date() == date_component
		assert reminder_date.microsecond == 0
		assert reminder_date.second == 0
		assert reminder_date.minute % 5 == 0
		assert reminder_date.hour == (now + timedelta(hours=1, minutes=(5 - now.minute % 5) % 5)).hour

		# Rounded up to the nearest 5 minute mark
		assert reminder_date.minute == (now + timedelta(minutes=(5 - now.minute % 5) % 5)).minute

	@pytest.mark.usefixtures("mock_2_hour_reminder_today_offset")
	def test_default_time_today_custom_offset(self):
		date_component = _today
		now = datetime.now()
		reminder_date = TaskParser.reminder_date_combine(date_component)

		assert reminder_date.date() == date_component
		assert reminder_date.microsecond == 0
		assert reminder_date.second == 0
		assert reminder_date.minute % 5 == 0
		assert reminder_date.hour == (now + timedelta(hours=2, minutes=(5 - now.minute % 5) % 5)).hour

		# Rounded up to the nearest 5 minute mark
		assert reminder_date.minute == (now + timedelta(minutes=(5 - now.minute % 5) % 5)).minute


	@pytest.mark.usefixtures("mock_disabled_reminder_today_offset")
	def test_default_time_today_disabled_offset(self):
		date_component = _today
		now = datetime.now()
		reminder_date = TaskParser.reminder_date_combine(date_component)

		assert reminder_date.date() == date_component
		assert reminder_date.time() == _default_reminder_time

#
# Lists
#

@pytest.mark.usefixtures("mock_lists")
class TestLists():

	def test_list_name_exact_match(self):
		target_list = _single_word_list
		title = 'a sample task'
		phrase = '%s: %s' % (target_list, title) # Finances: a sample task
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_infix_list_name_exact_match(self):
		target_list = _single_word_list
		title = 'a sample task'
		phrase = '%s in %s' % (title, target_list) # a sample task in Finances
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_list_name_diacritic_exact_match(self):
		target_list = _diacritic_list
		title = 'a sample task'
		phrase = '%s: %s' % (target_list, title) # Jardinería: a sample task
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_list_substring_prefix(self):
		target_list = _single_word_list
		title = 'a sample task'
		phrase = '%s: %s' % (target_list[:3], title) # Fin: a sample task
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_list_substring_infix(self):
		target_list = _single_word_list
		title = 'a sample task'
		phrase = '%s: %s' % (target_list[2:5], title) # nan: a sample task
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_list_initials(self):
		target_list = _multi_word_list
		title = 'a sample task'
		phrase = '%s: %s' % (initials(target_list), title) # SL: a sample task
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_infix_list_initials(self):
		target_list = _multi_word_list
		title = 'a sample task'
		phrase = '%s in list %s' % (title, initials(target_list)) # a sample task in list SL
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_infix_list_initials_ignored_if_lowercase(self):
		"""
		Fewer than 3 characters should be ignored unless uppercase
		"""
		target_list = _multi_word_list
		title = 'a sample task'
		phrase = '%s in %s' % (title, initials(target_list).lower()) # a sample task in sl
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=phrase)

	def test_list_name_case_insensitive_match(self):
		target_list = _single_word_list
		title = 'a sample task'
		phrase = '%s: %s' % (target_list.upper(), title) # FINANCES: a sample task
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_list_name_diacritic_insensitive_match(self):
		target_list = _diacritic_list
		title = 'a sample task'
		phrase = '%s: %s' % (_diacritic_list_insensitive, title) # Jardineria: a sample task (no accent)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_infix_list_name_containing_infix_keyword(self):
		"""
		Very contrived, but the point is that if a list contains "in" we need
		to match the entire phrase that was meant to be the list keyword,
		rather than matching a part of the list and leaving a part of the list
		in the task title
		"""
		target_list = _diacritic_list
		list_phrase = 'in jard in eria'
		title = 'a sample task'
		phrase = '%s: %s' % (_diacritic_list_insensitive, title) # Jardineria: a sample task (no accent)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

	def test_ignores_unknown_list_name(self):
		title = 'not a list: a sample task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_ignores_unknown_infix_list_name(self):
		title = 'a sample task in not a list'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_list_prompt(self):
		title = 'a sample task'
		phrase = ': %s' % (title)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, has_list_prompt=True)

	def test_infix_list_does_not_prompt(self):
		title = 'a sample task in'
		phrase = '%s ' % (title)
		task = TaskParser(phrase)

		assert_task(task, phrase=title, title=title, has_list_prompt=False)

#
# Hashtags
# 

class TestHashtags():

	def test_hashtag_prompt(self):
		title = 'a sample task #'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, has_hashtag_prompt=True)

	def test_hashtag_prompt_in_word_is_ignored(self):
		title = 'a sample task#'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_hashtag_prompt_in_word_following_unicode_character_is_ignored(self):
		title = 'a sample taskü#'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	@pytest.mark.usefixtures("mock_lists")
	def test_hashtag_prompt_following_list(self):
		target_list = _single_word_list
		title = '#'
		phrase = '%s:%s' % (target_list, title)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list), has_hashtag_prompt=True)
	
#
# Due date
# 

class TestDueDate():

	def test_due_date_formats(self):
		for (due_phrase, due_date) in due_date_formats.iteritems():
			title = 'a sample task'
			phrase = '%s %s' % (title, due_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_due_date_formats_with_keyword(self):
		for (due_phrase, due_date) in due_date_formats.iteritems():
			due_phrase = 'due ' + due_phrase
			title = 'a sample task'
			phrase = '%s %s' % (title, due_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_due_date_formats_with_keyword_and_filler_text(self):
		for (due_phrase, due_date) in due_date_formats.iteritems():
			due_phrase = 'due any filler text ' + due_phrase
			title = 'a sample task'
			phrase = '%s %s' % (title, due_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_explicit_due_date(self):
		title = 'a sample task'
		due_phrase = 'due 12/13/14'
		due_date = _12_13_14
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_case_insensitive_due_date(self):
		title = 'a sample task'
		due_phrase = 'DUe 12/13/14'
		due_date = _12_13_14
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_relative_due_date(self):
		title = 'a sample task'
		due_phrase = 'due today'
		due_date = date.today()
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

	def test_implicit_due_date(self):
		title = 'a sample task'
		due_phrase = 'tomorrow'
		due_date = _tomorrow
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

	@pytest.mark.usefixtures("mock_disabled_explicit_keywords")
	def test_implicit_due_date_disabled_in_prefs(self):
		due_phrase = 'tomorrow'
		title = 'a sample task %s' % due_phrase
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_due_next_year(self):
		"""
		The "next" word was not understood by parsedatetime.nlp() in an
		earlier version and the implementation in the workflow was incorrect;
		rather than the same date one year from now, "next year" means Jan 1
		of the following year.
		"""
		today = date.today()
		title = 'a sample task'
		due_phrase = 'due next year'
		due_date = date(year=today.year + 1, month=1, day=1)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_due_in_a_year(self):
		"""
		Due on this date, one year from now.

		This test would fail if run on Feb 29, so it will not run on that
		date.
		"""
		due_date = date.today()

		# Do not attempt on Feb 29 because that date will not exist next year
		if due_date.month != 2 or due_date.day != 29:
			title = 'a sample task'
			due_phrase = 'due in a year'
			due_date = due_date.replace(year=due_date.year + 1)
			phrase = '%s %s' % (title, due_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_due_next_weekday(self):
		# Get the day name 8 days from now. If today is Friday, due_date will
		# be not tomorrow but the following Saturday and weekday will be
		# "Saturday"
		due_date = date.today() + timedelta(days=8)

		# Since Sunday is the last day of the week in Python, "next Monday"
		# will actually correspond to the very next day rather than a week
		# later as expected. TODO: remove this workaround if fixed in
		# parsedatetime, but otherwise the test will always fail on Sunday.
		if date.today().weekday() == 6:
			due_date = date.today() + timedelta(days=1)

		weekday = due_date.strftime('%A')

		title = 'a sample task'
		due_phrase = 'due next %s' % (weekday)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

	def test_time_only_due_today_with_reminder(self):
		title = 'a sample task'
		due_phrase = 'due 12:00'
		due_date = _today
		reminder_date = datetime.combine(_today, _noon)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	def test_time_only_due_today_with_reminder_no_keyword(self):
		title = 'a sample task'
		due_phrase = 'at noon'
		due_date = _today
		reminder_date = datetime.combine(_today, _noon)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	def test_due_date_with_time_sets_reminder(self):
		title = 'a sample task'
		due_phrase = 'due 12/13/14 at noon'
		due_date = _12_13_14
		reminder_date = datetime.combine(due_date, _noon)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	def test_due_keyword_without_date(self):
		title = 'We are due for some rain'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_due_date_prompt_ignored_after_unicode_character(self):
		title = 'a sample tasküdue'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_due_date_prompt_following(self):
		title = 'a sample task'
		due_phrase = 'due'
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, has_due_date_prompt=True)

	def test_due_date_prompt_with_star(self):
		title = 'a sample task'
		due_phrase = 'due'
		phrase = '%s %s*' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, has_due_date_prompt=True, starred=True)

	def test_due_date_prompt_with_star_whitespace(self):
		title = 'a sample task'
		due_phrase = 'due'
		phrase = '%s %s *' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, has_due_date_prompt=True, starred=True)

	def test_implicit_due_date_disabled_in_task(self):
		due_phrase = 'tomorrow'
		title = 'a sample task %s' % due_phrase
		not_due_phrase = 'not due'
		phrase = '%s %s' % (title, not_due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_explicit_due_date_disabled_in_task(self):
		due_phrase = 'due tomorrow'
		title = 'a sample task %s' % due_phrase
		not_due_phrase = 'not due'
		phrase = '%s %s' % (title, not_due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_explicit_due_date_with_time_disabled_in_task(self):
		due_phrase = 'due at 4pm tomorrow'
		title = 'a sample task %s' % due_phrase
		not_due_phrase = 'not due'
		phrase = '%s %s' % (title, not_due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

#
# Recurrence
# 

class TestRecurrence():

	def test_recurrence_implicitly_due_today(self):
		title = 'a sample task'
		recurrence_type = 'month'
		recurrence_count = 1
		recurrence_phrase = 'every ' + recurrence_type
		due_date = date.today()
		phrase = '%s %s' % (title, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_recurrence_types(self):
		recurrence_count = 1
		(due_phrase, due_date) = due_date_formats.items()[0]
		for (recurrence_phrase, recurrence_type) in recurrence_types.iteritems():
			title = 'a sample task'
			recurrence_phrase = 'every ' + recurrence_phrase
			phrase = '%s %s due %s' % (title, recurrence_phrase, due_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_plural_recurrence_types(self):
		recurrence_count = 2
		(due_phrase, due_date) = due_date_formats.items()[1]
		for (recurrence_phrase, recurrence_type) in recurrence_types.iteritems():
			title = 'a sample task'
			recurrence_phrase = 'every %d %ss' % (recurrence_count, recurrence_phrase)
			phrase = '%s due %s %s' % (title, due_phrase, recurrence_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_single_count_recurrence_phrases(self):
		"""
		These phrases do not use the `every` keyword, e.g. monthly oil change
		"""
		recurrence_count = 1
		(due_phrase, due_date) = due_date_formats.items()[1]
		for (recurrence_phrase, recurrence_type) in single_recurrence_types.iteritems():
			title = 'a sample task'
			recurrence_phrase = recurrence_phrase
			phrase = '%s due %s %s' % (title, due_phrase, recurrence_phrase)
			task = TaskParser(phrase)

			assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_case_insensitive_recurrence_types(self):
		(due_phrase, due_date) = due_date_formats.items()[0]
		title = 'a sample task'
		recurrence_count = 2
		recurrence_type = 'year'
		recurrence_phrase = 'REpeat EVerY %d %sS' % (recurrence_count, recurrence_type.upper())
		phrase = '%s %s %s' % (title, due_phrase, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_recurrence_with_explicit_date(self):
		title = 'a sample task'
		recurrence_count = 1
		due_date = date(_today.year, 12, 31)
		recurrence_type = 'year'
		recurrence_phrase = 'every December 31'
		phrase = '%s %s' % (title, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_recurrence_with_explicit_weekday(self):
		title = 'a sample task'
		recurrence_count = 1
		due_date = _monday
		recurrence_type = 'week'
		recurrence_phrase = 'every Monday'
		phrase = '%s %s' % (title, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

	def test_recurrence_with_explicit_weekday_and_reminder(self):
		title = 'a sample task'
		recurrence_count = 1
		due_date = _monday
		reminder_date = datetime.combine(_monday, _noon)
		recurrence_type = 'week'
		recurrence_phrase = 'every Monday at noon'
		phrase = '%s %s' % (title, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date, reminder_date=reminder_date)

	def test_recurrence_prompt(self):
		title = 'a sample task'
		recurrence_phrase = 'every'
		phrase = '%s %s' % (title, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, has_recurrence_prompt=True)

	def test_recurrence_prompt_ignored_after_unicode_character(self):
		title = 'a sample tasküevery'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)


#
# Reminders
#

class TestReminders():

	def test_reminder_implicitly_relative_to_today(self):
		title = 'a sample task'
		reminder_phrase = 'r noon'
		reminder_date = datetime.combine(_today, time(12, 0, 0))
		phrase = '%s %s' % (title, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, reminder_date=reminder_date)

	def test_reminder_implicitly_relative_to_today_no_time(self):
		title = 'a sample task'
		reminder_phrase = 'reminder'
		reminder_date = TaskParser.reminder_date_combine(_today) # Adds 1hr and rounds up to nearest 5m mark
		phrase = '%s %s' % (title, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, reminder_date=reminder_date, has_reminder_prompt=True)

	def test_reminder_prompt_ignored_after_unicode_character(self):
		"""
		This was matching as the "r" command due to the lack of unicode word
		boundary support in regex
		"""
		title = 'a sample für task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title)

	def test_reminder_implicitly_relative_to_due_date(self):
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due tomorrow'
		reminder_phrase = 'alarm at 8:00a'
		reminder_date = datetime.combine(due_date, time(8, 0, 0))
		phrase = '%s %s %s' % (title, due_phrase, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	def test_explicit_reminder_overrides_due_date_with_time(self):
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due tomorrow at noon'
		reminder_phrase = 'alarm at 8:00a'
		reminder_date = datetime.combine(due_date, time(8, 0, 0))
		phrase = '%s %s %s' % (title, due_phrase, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	def test_reminder_implicitly_relative_to_due_date_no_time(self):
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due tomorrow'
		reminder_phrase = 'r'
		reminder_date = datetime.combine(due_date, _default_reminder_time)
		phrase = '%s %s %s' % (title, due_phrase, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date, has_reminder_prompt=True)

	def test_reminder_explicit_date(self):
		title = 'a sample task'
		reminder_phrase = 'remind me at dinner on Dec 13, 2014'
		reminder_date = datetime.combine(_12_13_14, time(19, 0, 0))
		phrase = '%s %s' % (title, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, reminder_date=reminder_date)

	def test_reminder_explicit_date(self):
		title = 'a sample task'
		reminder_phrase = 'remind me Dec 13, 2014'
		reminder_date = datetime.combine(_12_13_14, _default_reminder_time)
		phrase = '%s %s' % (title, reminder_phrase)
		task = TaskParser(phrase)

	def test_reminder_with_time_implicitly_due_today(self):
		title = 'a sample task'
		reminder_phrase = 'at noon'
		reminder_date = datetime.combine(_today, _noon)
		due_date = _today
		phrase = '%s %s' % (title, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	@pytest.mark.usefixtures("mock_lists")
	def test_reminder_with_list(self):
		target_list = _single_word_list
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due tomorrow'
		reminder_phrase = 'alarm at 8:00a'
		reminder_date = datetime.combine(due_date, time(8, 0, 0))
		phrase = '%s:%s %s %s' % (target_list, title, due_phrase, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list), due_date=due_date, reminder_date=reminder_date)

	@pytest.mark.usefixtures("mock_enabled_automatic_reminders")
	def test_automatic_reminder_with_due_date(self):
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due tomorrow'
		reminder_date = datetime.combine(due_date, _default_reminder_time)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	@pytest.mark.usefixtures("mock_enabled_automatic_reminders")
	def test_explicit_reminder_overrides_automatic_reminder(self):
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due tomorrow'
		reminder_phrase = 'r 8am'
		reminder_date = datetime.combine(due_date, time(8, 0, 0))
		phrase = '%s %s %s' % (title, due_phrase, reminder_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)

	@pytest.mark.usefixtures("mock_enabled_automatic_reminders")
	def test_due_date_with_time_overrides_automatic_reminder(self):
		title = 'a sample task'
		due_date = _tomorrow
		due_phrase = 'due 8:00 tomorrow'
		reminder_date = datetime.combine(due_date, time(8, 0, 0))
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date, reminder_date=reminder_date)
#
# Star
#

class TestStarred():

	def test_starred(self):
		title = 'a sample task'
		phrase = '%s *' % title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, starred=True)

	def test_ignore_infix_asterisk(self):
		title = 'a sample * task'
		phrase = title
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, starred=False)

#
# Note
#

class TestNote():

	note_delimiter = '//'

	def test_note(self):
		title = 'a sample task'
		note = 'my note'
		phrase = '%s %s%s' % (title, self.note_delimiter, note)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, note=note)

	def test_note_with_whitespace(self):
		title = 'a sample task'
		note = 'my note'
		phrase = '%s %s %s' % (title, self.note_delimiter, note)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, note=note)

	def test_multiline_note(self):
		title = 'a sample task'
		source_note = 'my\ntest\tnote'
		note = 'my test note'
		phrase = '%s %s %s' % (title, self.note_delimiter, note)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, note=note)

	def test_note_with_star(self):
		title = 'a sample task'
		note = 'my note'
		phrase = '%s* %s%s' % (title, self.note_delimiter, note)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, starred=True, note=note)

	def test_note_with_star_whitespace(self):
		title = 'a sample task'
		note = 'my note'
		phrase = '%s * %s%s' % (title, self.note_delimiter, note)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, starred=True, note=note)

#
# phrase_with()
#

class TestPhrases():

	task = None
	title = 'a sample task'

	@pytest.fixture(autouse=True)
	def setup_task(self):
		phrase = self.title
		self.task = TaskParser(phrase)

	def test_simple_unchanged_phrase(self):
		phrase = self.task.phrase
		new_phrase = self.task.phrase_with()

		assert phrase == new_phrase

	def test_complex_unchanged_phrase(self):
		phrase = 'fin: Oil change next Tuesday at noon repeat every 3mo *'
		task = TaskParser(phrase)
		new_phrase = task.phrase_with()

		assert phrase == new_phrase

	def test_phrase_reordering(self):
		"""
		This is not necessarily a desired feature compared to returning the
		same phrase the user entered, but it works for now.
		"""
		phrase = 'finances: r noon every 3mo Oil change next Tuesday *'
		target_phrase = 'finances: Oil change next Tuesday every 3mo r noon *'
		task = TaskParser(phrase)
		new_phrase = task.phrase_with()

		assert target_phrase == new_phrase

	def test_change_title(self):
		new_title = 'new title'
		new_phrase = self.task.phrase_with(title=new_title)

		assert new_phrase == '%s' % (new_title)

	def test_change_list_title(self):
		new_list_title = 'new title'
		new_phrase = self.task.phrase_with(list_title=new_list_title)

		assert new_phrase == '%s: %s' % (new_list_title, self.title)

	def test_change_due_date(self):
		new_due_date = 'due tomorrow'
		new_phrase = self.task.phrase_with(due_date=new_due_date)

		assert new_phrase == '%s %s' % (self.title, new_due_date)

	def test_change_recurrence(self):
		new_recurrence = 'every month'
		new_phrase = self.task.phrase_with(recurrence=new_recurrence)

		assert new_phrase == '%s %s' % (self.title, new_recurrence)

	def test_change_reminder(self):
		new_reminder = 'r tomorrow at noon'
		new_phrase = self.task.phrase_with(reminder_date=new_reminder)

		assert new_phrase == '%s %s' % (self.title, new_reminder)

	def test_add_reminder_prompt(self):
		new_reminder = 'remind me '
		new_phrase = self.task.phrase_with(reminder_date=True)

		assert new_phrase == '%s %s' % (self.title, new_reminder)

	def test_change_star(self):
		new_phrase = self.task.phrase_with(starred=True)

		assert new_phrase == '%s *' % (self.title)

	def test_prompt_list_title(self):
		new_phrase = self.task.phrase_with(list_title=True)

		assert new_phrase == ': %s' % (self.title)

	def test_prompt_due_date(self):
		new_phrase = self.task.phrase_with(due_date=True)

		assert new_phrase == '%s due ' % (self.title)

	def test_prompt_recurrence(self):
		new_phrase = self.task.phrase_with(recurrence=True)

		assert new_phrase == '%s every ' % (self.title)

	def test_add_hashtags(self):
		hashtag = 'Example'
		phrase = self.title
		task = TaskParser(phrase)

		new_phrase = self.task.phrase_with(hashtag=hashtag)

		assert new_phrase == '%s #%s' % (self.title, hashtag)

	def test_change_hashtags(self):
		hashtag = 'Example'
		phrase = '%s #' % self.title
		task = TaskParser(phrase)

		new_phrase = self.task.phrase_with(hashtag=hashtag)

		assert new_phrase == '%s #%s' % (self.title, hashtag)

	def test_remove_hashtag_prompt(self):
		hashtag = 'Example'
		phrase = '%s #%s' % (self.title, hashtag)
		task = TaskParser(phrase)

		new_phrase = self.task.phrase_with(hashtag=None)

		assert new_phrase == '%s' % (self.title)

