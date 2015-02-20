# encoding: utf-8

from wunderlist.models.task_parser import TaskParser
import pytest
import re
import locale
from datetime import date

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

def test_due_date():
	title = 'a sample task'
	due_phrase = 'due 12/13/14'
	due_date = date(2014, 12, 13)
	phrase = '%s %s' % (title, due_phrase)
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title, due_date=due_date)

def test_due_date_ignores_time():
	title = 'a sample task due 4:00'
	phrase = title
	task = TaskParser(phrase)

	assert_task(task, phrase=phrase, title=title)


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