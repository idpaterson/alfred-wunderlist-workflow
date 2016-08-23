from datetime import datetime
import os
import time

from workflow.notify import notify
from workflow.background import is_running

from wunderlist.models.preferences import Preferences
from wunderlist.util import workflow


def sync(background=False):
    from wunderlist.models import base, root, list, task, user, hashtag, reminder
    from peewee import OperationalError

    # If a sync is already running, wait for it to finish. Otherwise, store
    # the current pid in alfred-workflow's pid cache file
    if not background:
        if is_running('sync'):
            while is_running('sync'):
                time.sleep(.25)

            return False

        pidfile = workflow().cachefile('sync.pid')

        with open(pidfile, 'wb') as file_obj:
            file_obj.write('{0}'.format(os.getpid()))

    Preferences.current_prefs().last_sync = datetime.now()

    base.BaseModel._meta.database.create_tables([
        root.Root,
        list.List,
        task.Task,
        user.User,
        hashtag.Hashtag,
        reminder.Reminder
    ], safe=True)

    # Perform a query that requires the latest schema; if it fails due to a
    # mismatched scheme, delete the old database and re-sync
    try:
        task.Task.select().where(task.Task.recurrence_count > 0).count()
        hashtag.Hashtag.select().where(hashtag.Hashtag.tag == '').count()
    except OperationalError:
        base.BaseModel._meta.database.close()
        workflow().clear_data(lambda f: 'wunderlist.db' in f)

        sync()
        return

    first_sync = False

    try:
        root.Root.get()
    except root.Root.DoesNotExist:
        first_sync = True

    root.Root.sync(background=background)

    if background:
        if first_sync:
            notify('Initial sync has completed', 'All of your tasks are now available for browsing')

        # If executed manually, this will pass on to the post notification action
        print 'Sync completed successfully'

    return True


def background_sync():
    from workflow.background import run_in_background
    task_id = 'sync'

    # Only runs if another sync is not already in progress
    run_in_background(task_id, [
        '/usr/bin/env',
        'python',
        workflow().workflowfile('alfred-wunderlist-workflow.py'),
        'pref sync background',
        '--commit'
    ])


def background_sync_if_necessary():
    last_sync = Preferences.current_prefs().last_sync

    # Avoid syncing on every keystroke, background_sync will also prevent
    # multiple concurrent syncs
    if last_sync is None or (datetime.now() - last_sync).total_seconds() > 30:
        background_sync()
