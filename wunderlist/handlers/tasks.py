# encoding: utf-8

import re
from wunderlist.util import workflow
from parsedatetime import Calendar
from datetime import datetime

_calendar = u'📅'
_star = u'★'
_recurrence = u'↻'

_recurrence_pattern = r' every (\d*) ?((?:day|week|month)s?)'
_star_pattern = r'\*$'

def _task(args):
	return ' '.join(args)

def filter(args):
	task = _task(args)
	cal = Calendar()
	due_date = None
	starred = False
	list_name = 'Inbox'
	subtitle = []

	recurrence = re.search(_recurrence_pattern, task)
	if recurrence:
		task = re.sub(_recurrence_pattern, '', task)

	dates = cal.nlp(task)

	# Only remove the last date for now
	if dates:
		info = dates[-1]
		due_date = info[0]
		task = task.replace(info[4], '', 1)
		task = task.replace('due ', '')
	elif recurrence:
		due_date = datetime.today()

	if re.search(_star_pattern, task):
		starred = True
		task = re.sub(_star_pattern, '', task)
		subtitle.append(_star)

	if due_date:
		now = datetime.now()
		if due_date.date() == now.date():
			date_format = 'Today'
		if due_date.year == now.year:
			date_format = '%a, %b %d'
		else:
			date_format = '%b %d, %Y'

		subtitle.append('%s Due %s' % (_calendar, due_date.strftime(date_format)))

	if recurrence:
		subtitle.append(u'%s Every %d %s' % (_recurrence, int(recurrence.group(1) or 1), recurrence.group(2)))

	subtitle.append(task)

	workflow().add_item('Add Task to ' + list_name, '   '.join(subtitle), valid=True, modifier_subtitles={'alt': 'Select task before adding'})

	workflow().add_item('Assign to list', 'Prefix the task, e.g. Automotive: ' + task, autocomplete=': ' + task)
	workflow().add_item('Set a due date', '"due" followed by any date-related phrase, e.g. due next Tuesday; due May 4', autocomplete=task.strip() + ' due ')
	workflow().add_item('Make it a recurring task', '"every" followed by a unit of time, e.g. every 2 months; every year', autocomplete=task.strip() + ' every ')

	if starred:
		workflow().add_item('Unstar', 'Remove * from the task', autocomplete=' '.join(args).replace('*', ''))
	else:
		workflow().add_item('Star', 'End the task with * (asterisk)'
			, autocomplete=' '.join(args) + ' *')

def commit(args):
	from wunderlist.api import tasks
	list_id = args[0]
	task = _task(args[1:])

	tasks.create_task(list_id, task)