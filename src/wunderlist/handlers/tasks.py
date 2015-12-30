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

	if task.reminder_date:
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
	task = _task(args)
	subtitle = task_subtitle(task)
	wf = workflow()
	matching_hashtags = []

	if not task.title:
		subtitle = 'Begin typing to add a new task'

	# Preload matching hashtags into a list so that we can get the length
	if task.has_hashtag_prompt:
		from wunderlist.models.hashtag import Hashtag

		hashtags = Hashtag.select().where(Hashtag.id.contains(task.hashtag_prompt))

		for hashtag in hashtags:
			matching_hashtags.append(hashtag)

	# Show hashtag prompt if there is more than one matching hashtag or the
	# hashtag being typed does not exactly match the single matching hashtag
	if task.has_hashtag_prompt and len(matching_hashtags) > 0 and (len(matching_hashtags) > 1 or task.hashtag_prompt != matching_hashtags[0].id):
		for hashtag in matching_hashtags:
			wf.add_item(hashtag.id[1:], '', autocomplete=' ' + task.phrase_with(hashtag=hashtag.id) + ' ', icon=icons.HASHTAG)

	elif task.has_list_prompt:
		lists = wf.stored_data('lists')
		if lists:
			for list in lists:
				# Show some full list names and some concatenated in command
				# suggestions
				sample_command = list['title']
				if random() > 0.5:
					sample_command = sample_command[:int(len(sample_command) * .75)]
				icon = icons.INBOX if list['list_type'] == 'inbox' else icons.LIST
				wf.add_item(list['title'], 'Assign task to this list, e.g. %s: %s' % (sample_command.lower(), task.title), autocomplete=' ' + task.phrase_with(list_title=list['title']), icon=icon)
			wf.add_item('Remove list', 'Tasks without a list are added to the Inbox', autocomplete=' ' + task.phrase_with(list_title=False), icon=icons.CANCEL)
		elif is_running('sync'):
			wf.add_item('Your lists are being synchronized', 'Please try again in a few moments', autocomplete=' ' + task.phrase_with(list_title=False), icon=icons.BACK)
	
	# Task has an unfinished recurrence phrase
	elif task.has_recurrence_prompt:
		wf.add_item('Every month', 'Same day every month, e.g. every mo', uid="recurrence_1m", autocomplete=' %s ' % task.phrase_with(recurrence='every month'), icon=icons.RECURRENCE)
		wf.add_item('Every week', 'Same day every week, e.g. every week, every Tuesday', uid="recurrence_1w", autocomplete=' %s ' % task.phrase_with(recurrence='every week'), icon=icons.RECURRENCE)
		wf.add_item('Every year', 'Same date every year, e.g. every 1 y, every April 15', uid="recurrence_1y", autocomplete=' %s ' % task.phrase_with(recurrence='every year'), icon=icons.RECURRENCE)
		wf.add_item('Every 3 months', 'Same day every 3 months, e.g. every 3 months', uid="recurrence_3m", autocomplete=' %s ' % task.phrase_with(recurrence='every 3 months'), icon=icons.RECURRENCE)
		wf.add_item('Remove recurrence', autocomplete=' ' + task.phrase_with(recurrence=False), icon=icons.CANCEL)

	# Task has an unfinished due date phrase
	elif task.has_due_date_prompt:
		wf.add_item('Today', 'e.g. due today', autocomplete=' %s ' % task.phrase_with(due_date='due today'), icon=icons.TODAY)
		wf.add_item('Tomorrow', 'e.g. due tomorrow', autocomplete=' %s ' % task.phrase_with(due_date='due tomorrow'), icon=icons.TOMORROW)
		wf.add_item('Next Week', 'e.g. due next week', autocomplete=' %s ' % task.phrase_with(due_date='due next week'), icon=icons.NEXT_WEEK)
		wf.add_item('Next Month', 'e.g. due next month', autocomplete=' %s ' % task.phrase_with(due_date='due next month'), icon=icons.CALENDAR)
		wf.add_item('Next Year', 'e.g. due next year, due April 15', autocomplete=' %s ' % task.phrase_with(due_date='due next year'), icon=icons.CALENDAR)
		wf.add_item('Remove due date', 'Add "not due" to fix accidental dates, or see wl:pref', autocomplete=' ' + task.phrase_with(due_date=False), icon=icons.CANCEL)

	# Task has an unfinished reminder phrase
	elif task.has_reminder_prompt:
		prefs = Preferences.current_prefs()
		default_reminder_time = format_time(prefs.reminder_time, 'short')
		due_date_hint = ' on the due date' if task.due_date else ''
		wf.add_item('Reminder at %s%s' % (default_reminder_time, due_date_hint), 'e.g. r %s' % default_reminder_time, autocomplete=' %s ' % task.phrase_with(reminder_date='remind me at %s' % format_time(prefs.reminder_time, 'short')), icon=icons.REMINDER)
		wf.add_item('At noon%s' % due_date_hint, 'e.g. reminder noon', autocomplete=' %s ' % task.phrase_with(reminder_date='remind me at noon'), icon=icons.REMINDER)
		wf.add_item('At 8:00 PM%s' % due_date_hint, 'e.g. remind at 8:00 PM', autocomplete=' %s ' % task.phrase_with(reminder_date='remind me at 8:00pm'), icon=icons.REMINDER)
		wf.add_item('At dinner%s' % due_date_hint, 'e.g. alarm at dinner', autocomplete=' %s ' % task.phrase_with(reminder_date='remind me at dinner'), icon=icons.REMINDER)
		wf.add_item('Today at 6:00 PM', 'e.g. remind me today at 6pm', autocomplete=' %s ' % task.phrase_with(reminder_date='remind me today at 6:00pm'), icon=icons.REMINDER)
		wf.add_item('Remove reminder', autocomplete=' ' + task.phrase_with(reminder_date=False), icon=icons.CANCEL)

	# Main menu for tasks
	else:
		wf.add_item(task.list_title + u' – create a new task...', subtitle, arg='--stored-query', valid=task.title != '', icon=icons.TASK)

		title = 'Change list' if task.list_title else 'Select a list'
		wf.add_item(title, 'Prefix the task, e.g. Automotive: ' + task.title, autocomplete=' ' + task.phrase_with(list_title=True), icon=icons.LIST)

		title = 'Change the due date' if task.due_date else 'Set a due date'
		wf.add_item(title, '"due" followed by any date-related phrase, e.g. due next Tuesday; due May 4', autocomplete=' ' + task.phrase_with(due_date=True), icon=icons.CALENDAR)

		title = 'Change the recurrence' if task.recurrence_type else 'Make it a recurring task'
		wf.add_item(title, '"every" followed by a unit of time, e.g. every 2 months; every year; every 4w', autocomplete=' ' + task.phrase_with(recurrence=True), icon=icons.RECURRENCE)

		title = 'Change the reminder' if task.reminder_date else 'Set a reminder'
		wf.add_item(title, '"remind me" followed by a time and/or date, e.g. remind me at noon; r 10am; alarm 8:45p', autocomplete=' ' + task.phrase_with(reminder_date=True), icon=icons.REMINDER)

		if task.starred:
			wf.add_item('Remove star', 'Remove * from the task', autocomplete=' ' + task.phrase_with(starred=False), icon=icons.STAR_REMOVE)
		else:
			wf.add_item('Star', 'End the task with * (asterisk)', autocomplete=' ' + task.phrase_with(starred=True), icon=icons.STAR)

		if task.phrase:
			for t in Task.search(task.phrase):
				wf.add_item('Incomplete task in ' + t.list.title, task_subtitle(t), autocomplete=' ' + task.phrase_with(starred=True), icon=icons.TASK)

		wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args):
	from wunderlist.api import tasks

	task = _task(args)

	tasks.create_task(task.list_id, task.title, assignee_id=task.assignee_id,
		recurrence_type=task.recurrence_type, recurrence_count=task.recurrence_count,
		due_date=task.due_date, reminder_date=task.reminder_date, starred=task.starred,
		completed=task.completed
	)

	# Output must be a UTF-8 encoded string
	print ('The task was added to ' + task.list_title).encode('utf-8')
