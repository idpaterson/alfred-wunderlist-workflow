# encoding: utf-8

from wunderlist import icons
from wunderlist.util import workflow, format_time
from wunderlist.models.task import Task
from datetime import date, timedelta
import re

_star = u'★'
_overdue_1x = u'⚠️'
_overdue_2x = u'❗️'
_recurrence = u'↻'
_reminder = u'⏰'

_hashtag_prompt_pattern = r'#\S*$'

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

	conditions = None

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
	).order_by(Task.due_date.asc())
	tasks = sorted(tasks, key=lambda t: -t.overdue_times)

	for t in tasks:
		wf.add_item(u'%s – %s' % (t.list_title, t.title), task_subtitle(t), autocomplete=':task %s  ' % t.id, icon=icons.TASK_COMPLETED if t.completed_at else icons.TASK)

	wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args, modifier=None):
	pass
