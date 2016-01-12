from wunderlist.models.preferences import Preferences
from datetime import datetime

def sync():
	from wunderlist.models import base, root, list, task, user, hashtag, reminder

	Preferences.current_prefs().last_sync = datetime.now()

	base.BaseModel._meta.database.create_tables([
		root.Root,
		list.List,
		task.Task,
		user.User,
		hashtag.Hashtag,
		reminder.Reminder
	], safe=True)

	root.Root.sync()

	# If executed manually, this will pass on to the post notification action
	print 'Sync completed successfully'

def backgroundSync():
	from workflow.background import run_in_background
	from wunderlist.util import workflow

	# Only runs if another sync is not already in progress
	run_in_background('sync', [
		'/usr/bin/env',
		'python',
		workflow().workflowfile('alfred-wunderlist-workflow.py'),
		':pref sync',
		'--commit'
	])

def backgroundSyncIfNecessary():
	last_sync = Preferences.current_prefs().last_sync

	# Avoid syncing on every keystroke, backgroundSync will also prevent
	# multiple concurrent syncs
	if last_sync is None or (datetime.now() - last_sync).total_seconds() > 2:
		backgroundSync()
