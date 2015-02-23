def sync():
	from wunderlist.models import base, root, list, task, user

	existing_tables = base.BaseModel._meta.database.get_tables()

	base.BaseModel._meta.database.create_tables([
		root.Root,
		list.List,
		task.Task,
		user.User
	], safe=True)

	root.Root.sync()

	if not existing_tables:
		import subprocess
		subprocess.call(['/usr/bin/env', 'osascript', '-e', 'display notification "Your lists are now synchronized" with title "Initial Sync complete"'])

def backgroundSync():
	from workflow.background import run_in_background
	from wunderlist.util import workflow

	# Only runs if another sync is not already in progress
	run_in_background('sync', [
		'/usr/bin/env',
		'python',
		workflow().workflowfile('alfred-wunderlist-workflow.py'),
		'sync',
		'--commit'
	])