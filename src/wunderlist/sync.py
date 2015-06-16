def sync():
	from wunderlist.models import base, root, list, task, user, hashtag

	base.BaseModel._meta.database.create_tables([
		root.Root,
		list.List,
		task.Task,
		user.User,
		hashtag.Hashtag
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
		':sync',
		'--commit'
	])