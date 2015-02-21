from wunderlist.auth import is_authorized
from wunderlist.util import workflow

def route(args):
	handler = None
	command = ''

	if args:
		command = args[0].split(' ')

	if not is_authorized():
		from wunderlist.handlers import login
		handler = login
	elif 'list' in command:
		from wunderlist.handlers import lists
		handler = lists
	elif 'logout' in command:
		from wunderlist.handlers import logout
		handler = logout
	elif 'pref' in command or 'sync' in command:
		from wunderlist.handlers import preferences
		handler = preferences
	elif not command or not command[0]: 
		from wunderlist.handlers import welcome
		handler = welcome
	else:
		from wunderlist.handlers import tasks
		handler = tasks

	if handler:
		if '--commit' in args:
			handler.commit(command)
		else:
			handler.filter(command)

	workflow().send_feedback()