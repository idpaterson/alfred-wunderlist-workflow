from wunderlist.auth import is_authorized
from wunderlist.util import workflow

def route(args):
	handler = None
	command = []
	action = ''

	if args:
		command = args[0].split(' ')

	if command:
		action = command[0]

	if not is_authorized():
		from wunderlist.handlers import login
		handler = login
	elif action == ':list':
		from wunderlist.handlers import lists
		handler = lists
	elif action == ':logout':
		from wunderlist.handlers import logout
		handler = logout
	elif action == ':pref' or action == ':sync':
		from wunderlist.handlers import preferences
		handler = preferences
	elif len(command) <= 1 and not action: 
		from wunderlist.handlers import welcome
		handler = welcome
	# With no special keywords, the workflow creates a new task
	else:
		from wunderlist.handlers import tasks
		handler = tasks

	if handler:
		if '--commit' in args:
			handler.commit(command)
		else:
			handler.filter(command)

	workflow().send_feedback()