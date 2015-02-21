# encoding: utf-8

from wunderlist.models.task_parser import TaskParser
import pytest
import re
import locale
from datetime import date, timedelta

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

@pytest.fixture(autouse=True)
def mock_lists(mocker):
	"""
	Causes stored_data to return the lists specified for this test suite
	"""
	lists = map(lambda (i, title): { 'title': title, 'id': i }, enumerate(_lists))
	mocker.patch('workflow.Workflow.stored_data', new=lambda *arg:lists)

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

def assert_task(task, phrase=None, title=None, list_id=None, list_title=None, due_date=None, recurrence_type=None, recurrence_count=None, assignee_id=None, starred=False, completed=False, has_list_prompt=False, has_due_date_prompt=False, has_recurrence_prompt=False):
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
	assert task.assignee_id == assignee_id
	assert task.starred == starred
	assert task.completed == completed
	assert task.has_list_prompt == has_list_prompt
	assert task.has_due_date_prompt == has_due_date_prompt
	assert task.has_recurrence_prompt == has_recurrence_prompt

#
# Basics
#

def test_blank_phrase():
	phrase = ''
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=phrase)

def test_title():
	title = 'a sample task'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title)

def test_phrase_is_trimmed():
	title = 'a sample task'
	phrase = title
	task = TaskParser(' %s ' % phrase)

	assert_task(task, phrase=phrase, title=title)

def test_inbox_is_default():
	target_list = _inbox
	title = 'a sample task'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

#
# Lists
#

def test_list_name_exact_match():
	target_list = _single_word_list
	title = 'a sample task'
	phrase = '%s: %s' % (target_list, title) # Finances: a sample task
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_name_diacritic_exact_match():
	target_list = _diacritic_list
	title = 'a sample task'
	phrase = '%s: %s' % (target_list, title) # Jardinería: a sample task
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_substring_prefix():
	target_list = _single_word_list
	title = 'a sample task'
	phrase = '%s: %s' % (target_list[:3], title) # Fin: a sample task
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_substring_infix():
	target_list = _single_word_list
	title = 'a sample task'
	phrase = '%s: %s' % (target_list[2:5], title) # nan: a sample task
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_initials():
	target_list = _multi_word_list
	title = 'a sample task'
	phrase = '%s: %s' % (initials(target_list), title) # SL: a sample task
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_name_case_insensitive_match():
	target_list = _single_word_list
	title = 'a sample task'
	phrase = '%s: %s' % (target_list.upper(), title) # FINANCES: a sample task
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_name_diacritic_insensitive_match():
	target_list = _diacritic_list
	title = 'a sample task'
	phrase = '%s: %s' % (_diacritic_list_insensitive, title) # Jardineria: a sample task (no accent)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, list_title=target_list, list_id=_lists.index(target_list))

def test_list_prompt():
	title = 'a sample task'
	phrase = ': %s' % (title)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, has_list_prompt=True)
	
#
# Due date
# 

_12_13_14 = date(2014, 12, 13)
_today = date.today()
_tomorrow = date.today() + timedelta(days=1)
_next_week = date.today() + timedelta(days=7)
due_date_formats = {
	'12/13/14': _12_13_14,
	'12/13/2014': _12_13_14,
	'Dec 13, 2014': _12_13_14,
	'December 13, 2014': _12_13_14,
	'Dec 13th 2014': _12_13_14,
	'tomorrow': _tomorrow,
	'1d': _tomorrow,
	'next week': _next_week,
	'1w': _next_week,
	'in 1 week': _next_week,
	'in 7d': _next_week
}

def test_due_date_formats():
	for (due_phrase, due_date) in due_date_formats.iteritems():
		title = 'a sample task'
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_due_date_formats_with_keyword():
	for (due_phrase, due_date) in due_date_formats.iteritems():
		due_phrase = 'due ' + due_phrase
		title = 'a sample task'
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_due_date_formats_with_keyword_and_filler_text():
	for (due_phrase, due_date) in due_date_formats.iteritems():
		due_phrase = 'due any filler text ' + due_phrase
		title = 'a sample task'
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_explicit_due_date():
	title = 'a sample task'
	due_phrase = 'due 12/13/14'
	due_date = _12_13_14
	phrase = '%s %s' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_case_insensitive_due_date():
	title = 'a sample task'
	due_phrase = 'DUe 12/13/14'
	due_date = _12_13_14
	phrase = '%s %s' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_relative_due_date():
	title = 'a sample task'
	due_phrase = 'due today'
	due_date = date.today()
	phrase = '%s %s' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_due_next_year():
	"""
	The "next" word was not understood by parsedatetime.nlp(), so "next week"
	is transformed to "in 1 week" before calling nlp.

	This test would fail if run on Feb 29.
	"""
	due_date = date.today()

	# Do not attempt on Feb 29 because that date will not exist next year
	if due_date.month != 2 or due_date.day != 29:
		title = 'a sample task'
		due_phrase = 'due next year'
		due_date = due_date.replace(year=due_date.year + 1)
		phrase = '%s %s' % (title, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_due_date_ignores_time():
	title = 'a sample task due 4:00'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title)

def test_due_date_ignores_time_no_keyword():
	title = 'a sample task 4:00'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title)

def test_due_keyword_without_date():
	title = 'We are due for some rain'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title)

def test_due_date_prompt():
	title = 'a sample task'
	due_phrase = 'due'
	phrase = '%s %s' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, has_due_date_prompt=True)

def test_due_date_prompt_with_star():
	title = 'a sample task'
	due_phrase = 'due'
	phrase = '%s %s*' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, has_due_date_prompt=True, starred=True)

def test_due_date_prompt_with_star_whitespace():
	title = 'a sample task'
	due_phrase = 'due'
	phrase = '%s %s *' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, has_due_date_prompt=True, starred=True)

#
# Recurrence
# 

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

def test_recurrence_implicitly_due_today():
	title = 'a sample task'
	recurrence_type = 'month'
	recurrence_count = 1
	recurrence_phrase = 'every ' + recurrence_type
	due_date = date.today()
	phrase = '%s %s' % (title, recurrence_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

def test_recurrence_types():
	recurrence_count = 1
	(due_phrase, due_date) = due_date_formats.items()[0]
	for (recurrence_phrase, recurrence_type) in recurrence_types.iteritems():
		title = 'a sample task'
		recurrence_phrase = 'every ' + recurrence_phrase
		phrase = '%s %s due %s' % (title, recurrence_phrase, due_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

def test_plural_recurrence_types():
	recurrence_count = 2
	(due_phrase, due_date) = due_date_formats.items()[1]
	for (recurrence_phrase, recurrence_type) in recurrence_types.iteritems():
		title = 'a sample task'
		recurrence_phrase = 'every %d %ss' % (recurrence_count, recurrence_phrase)
		phrase = '%s due %s %s' % (title, due_phrase, recurrence_phrase)
		task = TaskParser(phrase)

		assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

def test_case_insensitive_recurrence_types():
	(due_phrase, due_date) = due_date_formats.items()[0]
	title = 'a sample task'
	recurrence_count = 2
	recurrence_type = 'year'
	recurrence_phrase = 'REpeat EVerY %d %sS' % (recurrence_count, recurrence_type.upper())
	phrase = '%s %s %s' % (title, due_phrase, recurrence_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, recurrence_type=recurrence_type, recurrence_count=recurrence_count, due_date=due_date)

def test_recurrence_prompt():
	title = 'a sample task'
	recurrence_phrase = 'every'
	phrase = '%s %s' % (title, recurrence_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, has_recurrence_prompt=True)


#
# Star
#

def test_starred():
	title = 'a sample task'
	phrase = '%s *' % title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, starred=True)

def test_ignore_infix_asterisk():
	title = 'a sample * task'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, starred=False)