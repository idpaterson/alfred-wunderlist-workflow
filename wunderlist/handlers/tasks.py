# encoding: utf-8

from wunderlist.util import workflow
from wunderlist.models.task_parser import TaskParser
from datetime import date

_calendar = u'📅'
_star = u'★'
_recurrence = u'↻'

def _task(args):
	return TaskParser(' '.join(args))

def filter(args):
	task = _task(args)
	subtitle = []

	if task.starred:
		subtitle.append(_star)

	if task.due_date:
		today = date.today()
		if task.due_date == today:
			date_format = 'Today'
		if task.due_date.year == today.year:
			date_format = '%a, %b %d'
		else:
			date_format = '%b %d, %Y'

		subtitle.append('%s Due %s' % (_calendar, task.due_date.strftime(date_format)))

	if task.recurrence_type:
		subtitle.append(u'%s Every %d %s%s' % (_recurrence, task.recurrence_count, task.recurrence_type, 's' if task.recurrence_count != 1 else ''))

	subtitle.append(task.title or 'Begin typing to add a new task')

	workflow().add_item('Add Task to ' + task.list_title, '   '.join(subtitle), arg=task.phrase, valid=True)

	workflow().add_item('Assign to list', 'Prefix the task, e.g. Automotive: ' + task.title, autocomplete=task.phrase_with(list_title=True))
	workflow().add_item('Set a due date', '"due" followed by any date-related phrase, e.g. due next Tuesday; due May 4', autocomplete=task.phrase_with(due_date=True))
	workflow().add_item('Make it a recurring task', '"every" followed by a unit of time, e.g. every 2 months; every year; every 4w', autocomplete=task.phrase_with(recurrence=True))

	if task.starred:
		workflow().add_item('Unstar', 'Remove * from the task', autocomplete=task.phrase_with(starred=False))
	else:
		workflow().add_item('Star', 'End the task with * (asterisk)'
			, autocomplete=task.phrase_with(starred=True))

def commit(args):
	from wunderlist.api import tasks
	task = _task(args)

	# TODO: handle all the other task metadata
	tasks.create_task(task.list_id, task.title, assignee_id=task.assignee_id, 
		recurrence_type=task.recurrence_type, recurrence_count=task.recurrence_count, 
		due_date=task.due_date, starred=task.starred, completed=task.completed
	)