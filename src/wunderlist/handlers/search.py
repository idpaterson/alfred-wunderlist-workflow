# encoding: utf-8

from wunderlist import icons
from wunderlist.util import workflow, format_time
from wunderlist.models.task import Task
from datetime import date
import re

_star = u'★'
_recurrence = u'↻'
_reminder = u'⏰'

_hashtag_prompt_pattern = r'#\S*$'

def _task(args):
	return TaskParser(' '.join(args))

def task_subtitle(task):
	subtitle = []

	if task.starred:
		subtitle.append(_star)

	if task.due_date:
		today = date.today()
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

	if False and task.reminder_date:
		today = date.today()
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
	query = ' '.join(args[1:])
	wf = workflow()
	matching_hashtags = []

	if not query:
		wf.add_item('Begin typing to search tasks', '', icon=icons.SEARCH)

	hashtag_match = re.search(_hashtag_prompt_pattern, query)
	if hashtag_match:
		from wunderlist.models.hashtag import Hashtag

		hashtag_prompt = hashtag_match.group()
		hashtags = Hashtag.select().where(Hashtag.id.contains(hashtag_prompt))

		for hashtag in hashtags:
			# If there is an exact match, do not show hashtags
			if hashtag.id.lower() == hashtag_prompt.lower():
				matching_hashtags = []
				break

			matching_hashtags.append(hashtag)

	# Show hashtag prompt if there is more than one matching hashtag or the
	# hashtag being typed does not exactly match the single matching hashtag
	if len(matching_hashtags) > 0:
		for hashtag in matching_hashtags:
			wf.add_item(hashtag.id[1:], '', autocomplete=u':search %s %s ' % (query[:hashtag_match.start()], hashtag.id), icon=icons.HASHTAG)

	else:
		conditions = None

		for arg in args:
			if len(arg) > 1:
				conditions = conditions | Task.title.contains(arg)

		for t in Task.select().where(Task.completed_at.is_null() & Task.list.is_null(False) & conditions):
			wf.add_item(u'%s – %s' % (t.list_title, t.title), task_subtitle(t), autocomplete=':task %s  ' % t.id, icon=icons.TASK_COMPLETED if t.completed_at else icons.TASK)

		wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args, modifier=None):
	pass
