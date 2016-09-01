import os
import re

from wunderlist import icons
from wunderlist.auth import is_authorized
from wunderlist.sync import background_sync_if_necessary
from wunderlist.util import workflow


def route(args):
    handler = None
    command = []
    command_string = ''
    action = 'none'

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

    command_string = re.sub(r'^[^\w\s]+', '', command_string)
    command = re.split(r' +', command_string)

    if command:
        action = re.sub(r'^\W+', '', command[0]) or 'none'

    if 'about'.find(action) == 0:
        from wunderlist.handlers import about
        handler = about
    elif not is_authorized():
        from wunderlist.handlers import login
        handler = login
    elif 'list'.find(action) == 0:
        from wunderlist.handlers import lists
        handler = lists
    elif 'task'.find(action) == 0:
        from wunderlist.handlers import task
        handler = task
    elif 'search'.find(action) == 0:
        from wunderlist.handlers import search
        handler = search
    elif 'due'.find(action) == 0:
        from wunderlist.handlers import due
        handler = due
    elif 'upcoming'.find(action) == 0:
        from wunderlist.handlers import upcoming
        handler = upcoming
    elif 'logout'.find(action) == 0:
        from wunderlist.handlers import logout
        handler = logout
    elif 'pref'.find(action) == 0:
        from wunderlist.handlers import preferences
        handler = preferences
    # If the command starts with a space (no special keywords), the workflow
    # creates a new task
    elif not command_string:
        from wunderlist.handlers import welcome
        handler = welcome
    else:
        from wunderlist.handlers import new_task
        handler = new_task

    if handler:
        if '--commit' in args:
            modifier = re.search(r'--(alt|cmd|ctrl|fn)\b', ' '.join(args))

            if modifier:
                modifier = modifier.group(1)

            handler.commit(command, modifier)
        else:
            handler.filter(command)

            if workflow().update_available:
                update_data = workflow().cached_data('__workflow_update_status', max_age=0)

                if update_data.get('version') != '__VERSION__':
                    workflow().add_item('An update is available!', 'Update the Wunderlist workflow from version __VERSION__ to %s' % update_data.get('version'), arg='-about update', valid=True, icon=icons.DOWNLOAD)

            workflow().send_feedback()

    background_sync_if_necessary()
