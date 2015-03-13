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
	# If the command starts with a space (no special keywords), the workflow
	# creates a new task
	elif args[0] and args[0][0] == ' ':
		from wunderlist.handlers import tasks
		handler = tasks
	else:
		from wunderlist.handlers import welcome
		handler = welcome

	if handler:
		if '--commit' in args:
			handler.commit(command)
		else:
			handler.filter(command)

	workflow().send_feedback()