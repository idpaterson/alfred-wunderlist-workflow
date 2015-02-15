from wunderlist.api import tasks, lists
from wunderlist import util

def _task(args):
	return ' '.join(args)

def filter(args):
	for list in lists.lists():
		task = _task(args)
		arg = '%d %s' % (list['id'], task)
		util.workflow().add_item(list['title'], 'Add task: ' + task, arg=arg, valid=True)

def commit(args):
	list_id = args[0]
	task = _task(args[1:])

	tasks.create_task(list_id, task)