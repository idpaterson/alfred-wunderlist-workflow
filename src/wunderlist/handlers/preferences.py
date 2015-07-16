# encoding: utf-8

from wunderlist.models.user import User
from wunderlist.models.preferences import Preferences
from wunderlist.util import workflow, parsedatetime_calendar, parsedatetime_constants, format_time
from wunderlist import icons

def _parse_time(phrase):
	from datetime import time

	cal = parsedatetime_calendar()

	datetime_info = cal.parse(phrase)

	# Ensure that only a time was provided and not a date
	if datetime_info[1] == 2:
		return time(*datetime_info[0][3:5])
	return None

def filter(args):
	prefs = Preferences.current_prefs()

	if 'reminder' in args:
		reminder_time = _parse_time(' '.join(args))

		if reminder_time is not None:
			workflow().add_item(
				'Change default reminder time',
				u'⏰ %s' % format_time(reminder_time, 'short'),
				arg=' '.join(args), valid=True, icon=icons.REMINDER
			)
		else:
			workflow().add_item(
				'Type a new reminder time',
				'Date offsets like the morning before the due date are not supported yet',
				valid=False, icon=icons.REMINDER
			)

		workflow().add_item(
			'Cancel',
			autocomplete=':pref', icon=icons.BACK
		)
	else:
		current_user = User.get()

		if current_user and current_user.name:
			workflow().add_item(
				'Sign out',
				'You are logged in as ' + current_user.name,
				autocomplete=':logout', icon=icons.CANCEL
			)

		workflow().add_item(
			'Default reminder time',
			u'⏰ %s    Reminders without a specific time will be set to this time' % format_time(prefs.reminder_time, 'short'),
			autocomplete=':pref reminder ', icon=icons.REMINDER
		)

		workflow().add_item(
			'Require explicit due keyword',
			'Requires the due keyword to avoid accidental due date extraction',
			arg=':pref explicit_keywords', valid=True, icon=icons.TASK_COMPLETED if prefs.explicit_keywords else icons.TASK
		)

		workflow().add_item(
			'Force sync',
			'The workflow syncs automatically, but feel free to be forcible.',
			arg=':pref sync', valid=True, icon=icons.SYNC
		)

		workflow().add_item(
			'Switch theme',
			'Toggle between light and dark icons',
			arg=':pref retheme',
			valid=True,
			icon=icons.PAINTBRUSH
		)

		workflow().add_item(
			'Main menu',
			autocomplete='', icon=icons.BACK
		)

def commit(args):
	prefs = Preferences.current_prefs()
	relaunch_alfred = False

	if 'sync' in args:
		from wunderlist.sync import sync
		sync()
	elif 'explicit_keywords' in args:
		relaunch_alfred = True

		prefs.explicit_keywords = not prefs.explicit_keywords

		if prefs.explicit_keywords:
			print 'Remember to use the "due" keyword'
		else:
			print 'Implicit due dates enabled (e.g. "Recycling tomorrow")'
	elif 'reminder' in args:
		relaunch_alfred = True
		reminder_time = _parse_time(' '.join(args))

		if reminder_time is not None:
			prefs.reminder_time = reminder_time

			print 'Reminders will now default to %s' % format_time(reminder_time, 'short')
	elif 'retheme' in args:
		relaunch_alfred = True
		prefs.icon_theme = 'light' if icons.icon_theme() == 'dark' else 'dark'

		print 'The workflow is now using the %s icon theme' % (prefs.icon_theme)

	if relaunch_alfred:
		import subprocess
		subprocess.call(['/usr/bin/env', 'osascript', 'bin/launch_alfred.scpt', 'wl:pref'])
