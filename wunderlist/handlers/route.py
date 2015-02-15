from wunderlist.auth import is_authorized
from wunderlist.util import workflow

def route(args):
	handler = None

	if not is_authorized():
		from wunderlist.handlers import login
		handler = login
	elif 'list' in args:
		from wunderlist.handlers import lists
		handler = lists
	elif 'logout' in args:
		from wunderlist.handlers import logout
		handler = logout
	elif 'pref' in args:
		from wunderlist.handlers import preferences
		handler = preferences
	elif not args or not args[0]: 
		from wunderlist.handlers import welcome
		handler = welcome
	else:
		from wunderlist.handlers import tasks
		handler = tasks

	if handler:
		if '--commit' in args:
			args.remove('--commit')
			handler.commit(args)
		else:
			handler.filter(args)

	workflow().send_feedback()