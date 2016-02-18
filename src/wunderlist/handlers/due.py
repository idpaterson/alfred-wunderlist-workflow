# encoding: utf-8

from wunderlist import icons
from wunderlist.util import workflow, format_time
from wunderlist.models.task import Task
from wunderlist.models.list import List
from wunderlist.models.preferences import Preferences
from datetime import date, timedelta
import re

_star = u'★'
_overdue_1x = u'⚠️'
_overdue_2x = u'❗️'
_recurrence = u'↻'
_reminder = u'⏰'

_hashtag_prompt_pattern = r'#\S*$'

_due_orders = (
	{
		'due_order': ['order', 'due_date', 'list.order'],
		'title': 'Most overdue within each list',
		'subtitle': 'Sort tasks by increasing due date within lists (Wunderlist default)'
	},
	{
		'due_order': ['order', '-due_date', 'list.order'],
		'title': 'Most recently due within each list',
		'subtitle': 'Sort tasks by decreasing due date within lists'
	},
	{
		'due_order': ['order', 'due_date'],
		'title': 'Most overdue at the top',
		'subtitle': 'All tasks sorted by increasing due date'
	},
	{
		'due_order': ['order', '-due_date'],
		'title': 'Most recently due at the top',
		'subtitle': 'All tasks sorted by decreasing due date'
	}
)

def _task(args):
	return TaskParser(' '.join(args))

def task_subtitle(task):
	subtitle = []
	today = date.today()

	if task.starred:
		subtitle.append(_star)

	if task.due_date:
		if task.due_date == today:
			date_format = 'Today'
		elif task.due_date.year == today.year:
			date_format = '%a, %b %d'
		else:
			date_format = '%b %d, %Y'

		subtitle.append('Due %s' % (task.due_date.strftime(date_format)))

	if task.recurrence_type:
		if task.recurrence_count > 1:
			subtitle.append('%s Every %d %ss' % (_recurrence, task.recurrence_count, task.recurrence_type))
		# Cannot simply add -ly suffix
		elif task.recurrence_type == 'day':
			subtitle.append('%s Daily' % (_recurrence))
		else:
			subtitle.append('%s %sly' % (_recurrence, task.recurrence_type.title()))

	overdue_times = task.overdue_times
	if overdue_times > 1:
		subtitle.insert(0, u'%s %dX OVERDUE!' % (_overdue_2x, overdue_times))
	elif overdue_times == 1:
		subtitle.insert(0, u'%s OVERDUE!' % (_overdue_1x))

	if False and task.reminder_date:
		if task.reminder_date.date() == today:
			date_format = 'Today'
		elif task.reminder_date.date() == task.due_date:
			date_format = 'On due date'
		elif task.reminder_date.year == today.year:
			date_format = '%a, %b %d'
		else:
			date_format = '%b %d, %Y'

		subtitle.append('%s %s at %s' % (
			_reminder,	
			task.reminder_date.strftime(date_format),
			format_time(task.reminder_date.time(), 'short'))
		)

	subtitle.append(task.title)

	return '   '.join(subtitle)

def filter(args):
	wf = workflow()
	prefs = Preferences.current_prefs()
	command = args[1] if len(args) > 1 else None

	if command == 'sort':
		# Apply selected sort option
		if len(args) > 2:
			if args[2] == 'toggle-skipped':
				prefs.hoist_skipped_tasks = not prefs.hoist_skipped_tasks

				from workflow.background import run_in_background

				# Remove the sort command syntax. This is not done as a commit
				# action in the event that resetting the Alfred query does not
				# work due to accessibility settings.
				run_in_background('launch_alfred', ['/usr/bin/env', 'osascript', 'bin/launch_alfred.scpt', 'wl-due sort'])
			else:
				try:
					index = int(args[2])
					order_info = _due_orders[index - 1]
					prefs.due_order = order_info['due_order']

					from workflow.background import run_in_background

					# Remove the sort command syntax. This is not done as a commit
					# action in the event that resetting the Alfred query does not
					# work due to accessibility settings.
					run_in_background('launch_alfred', ['/usr/bin/env', 'osascript', 'bin/launch_alfred.scpt', 'wl-due'])

					# If resetting the alfred query does not work, make sure that the
					# due tasks are not searched by the sort command
					args = []
					command = None
				except:
					pass
		# Show sort options
		else:
			for i, order_info in enumerate(_due_orders):
				wf.add_item(order_info['title'], order_info['subtitle'], autocomplete='-due sort %d' % (i + 1), icon=icons.RADIO_SELECTED if order_info['due_order'] == prefs.due_order else icons.RADIO)

			wf.add_item('Highlight skipped recurring tasks', 'Hoists recurring tasks that have been missed multiple times over to the top', autocomplete='-due sort toggle-skipped', icon=icons.CHECKBOX_SELECTED if prefs.hoist_skipped_tasks else icons.CHECKBOX)

			wf.add_item('Back', autocomplete='-due ', icon=icons.BACK)

			return

	conditions = None

	# Build task title query based on the args
	for arg in args[1:]:
		if len(arg) > 1:
			conditions = conditions | Task.title.contains(arg)

	if conditions is None:
		conditions = True

	tasks = Task.select().where(
		Task.completed_at.is_null() &
		(Task.due_date < date.today() + timedelta(days=1)) &
		Task.list.is_null(False) &
		conditions
	)

	# Sort the tasks according to user preference
	for key in prefs.due_order:
		order = 'asc'
		field = None
		if key[0] == '-':
			order = 'desc'
			key = key[1:]

		if key == 'due_date':
			field = Task.due_date
		elif key == 'list.order':
			tasks = tasks.join(List)
			field = List.order
		elif key == 'order':
			field = Task.order

		if field:
			if order == 'asc':
				tasks = tasks.order_by(field.asc())
			else:
				tasks = tasks.order_by(field.desc())

	if prefs.hoist_skipped_tasks:
		tasks = sorted(tasks, key=lambda t: -t.overdue_times)

	for t in tasks:
		wf.add_item(u'%s – %s' % (t.list_title, t.title), task_subtitle(t), autocomplete='-task %s ' % t.id, icon=icons.TASK_COMPLETED if t.completed_at else icons.TASK)

	wf.add_item(u'Sort order', 'Change the display order of due tasks', autocomplete='-due sort', icon=icons.SORT)

	wf.add_item('Let\'s discuss this screen', 'Do you need a different sort order or list-level task controls?', arg=' '.join(args + ['discuss']), valid=True, icon=icons.DISCUSS)

	wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args, modifier=None):
	action = args[1] 

	if action == 'discuss':
		import webbrowser

		webbrowser.open('https://github.com/idpaterson/alfred-wunderlist-workflow/issues/96')
