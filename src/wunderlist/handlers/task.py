# encoding: utf-8

from wunderlist import icons
from wunderlist.util import workflow, format_time
from wunderlist.models.task_parser import TaskParser
from wunderlist.models.preferences import Preferences
from wunderlist.models.task import Task
from wunderlist.models.reminder import Reminder
from workflow.background import is_running
from datetime import date
from random import random

_star = u'★'
_recurrence = u'↻'
_reminder = u'⏰'

def _task(args):
	return TaskParser(' '.join(args))

def _modifier_subtitles(alt=None, cmd=None, ctrl=None, fn=None, shift=None):
	subtitles = {}

	if alt is not None:
		subtitles['alt'] = alt
	if cmd is not None:
		subtitles['cmd'] = cmd
	if ctrl is not None:
		subtitles['ctrl'] = ctrl
	if fn is not None:
		subtitles['fn'] = fn
	if shift is not None:
		subtitles['shift'] = shift

	return subtitles

def filter(args):
	task_id = args[1]
	task = Task.get(Task.id == task_id)
	wf = workflow()
	matching_hashtags = []

	if not task:
		wf.add_item('Unknown task', 'The ID does not match a task', icon=icons.BACK)
	else:
		if task.completed_at:
			wf.add_item(task.title, 'Mark task not completed', modifier_subtitles={
			}, arg=' '.join(args + ['toggle-completion']), valid=True, icon=icons.TASK_COMPLETED)
		else:
			wf.add_item(task.title, 'Complete this task', modifier_subtitles=_modifier_subtitles(
				alt='Complete this task and set due today'
			), arg=' '.join(args + ['toggle-completion']), valid=True, icon=icons.TASK)

		if task.recurrence_type and not task.completed_at:
			wf.add_item('Delete', 'Delete this task and cancel recurrence', arg=' '.join(args + ['delete']), valid=True, icon=icons.TRASH)
		else:
			wf.add_item('Delete', 'Delete this task', arg=' '.join(args + ['delete']), valid=True, icon=icons.TRASH)

		wf.add_item('Let\'s discuss this screen', 'What task-level features do you need here?', arg=' '.join(args + ['discuss']), valid=True, icon=icons.DISCUSS)

		wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args, modifier=None):
	from wunderlist.api import tasks
	
	task_id = args[1]
	action = args[2]
	task = Task.get(Task.id == task_id)

	if action == 'toggle-completion':
		due_date = task.due_date

		if modifier == 'alt':
			due_date = date.today()

		if task.completed_at:
			tasks.update_task(task.id, task.revision, completed=False, due_date=due_date)
			print 'The task was marked incomplete'
		else:
			tasks.update_task(task.id, task.revision, completed=True, due_date=due_date)
			print 'The task was marked complete'

	elif action == 'delete':
		if tasks.delete_task(task.id, task.revision):
			print 'The task was deleted'
		else:
			print 'Please try again'

	elif action == 'discuss':
		import webbrowser

		webbrowser.open('https://github.com/idpaterson/alfred-wunderlist-workflow/issues/94')
