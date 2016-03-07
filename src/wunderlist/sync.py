from wunderlist.models.preferences import Preferences
from datetime import datetime
from wunderlist.util import workflow

def sync():
    from wunderlist.models import base, root, list, task, user, hashtag, reminder
    from peewee import OperationalError

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
    except OperationalError:
        base.BaseModel._meta.database.close()
        workflow().clear_data(lambda f: 'wunderlist.db' in f)

        sync()
        return

    root.Root.sync()

    # If executed manually, this will pass on to the post notification action
    print 'Sync completed successfully'

def backgroundSync(force=False):
    from workflow.background import run_in_background
    task_id = 'sync'

    if force:
        task_id = 'forced_sync'

    # Only runs if another sync is not already in progress
    run_in_background(task_id, [
        '/usr/bin/env',
        'python',
        workflow().workflowfile('alfred-wunderlist-workflow.py'),
        'pref sync',
        '--commit'
    ])

def backgroundSyncIfNecessary():
    last_sync = Preferences.current_prefs().last_sync

    # Avoid syncing on every keystroke, backgroundSync will also prevent
    # multiple concurrent syncs
    if last_sync is None or (datetime.now() - last_sync).total_seconds() > 2:
        backgroundSync()
