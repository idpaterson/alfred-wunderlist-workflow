from wunderlist.auth import is_authorized
from wunderlist.util import workflow
from wunderlist import icons
import re
import os

def route(args):
	handler = None
	command = []
	command_string = ''
	action = ''

	# Read the stored query, which will correspond to the user's alfred query
	# as of the very latest keystroke. This may be different than the query
	# when this script was launched due to the startup latency.
	if args[0] == '--stored-query':
		query_file = workflow().workflowfile('.query')
		with open(query_file, 'r') as f:
			command_string = workflow().decode(f.read())
		os.remove(query_file)
	# Otherwise take the command from the first command line argument
	elif args:
		command_string = args[0]

	command = command_string.split(' ')

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
	elif command_string and command_string[0] == ' ':
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

			if workflow().update_available:
				workflow().add_item('An update is available!', 'Update the Wunderlist workflow to a newer version', arg=':pref update', valid=True, icon=icons.DOWNLOAD)

			workflow().send_feedback()
