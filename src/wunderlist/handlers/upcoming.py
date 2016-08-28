# encoding: utf-8

from datetime import date, datetime, timedelta

from peewee import JOIN, OperationalError
from workflow.background import is_running

from wunderlist import icons
from wunderlist.models.preferences import Preferences
from wunderlist.models.reminder import Reminder
from wunderlist.models.task import Task
from wunderlist.models.list import List
from wunderlist.sync import background_sync, background_sync_if_necessary, sync
from wunderlist.util import workflow

_hashtag_prompt_pattern = r'#\S*$'

_durations = [
    {
        'days': 7,
        'label': 'In the next week',
        'subtitle': 'Show tasks that are due in the next 7 days'
    },
    {
        'days': 14,
        'label': 'In the next 2 weeks',
        'subtitle': 'Show tasks that are due in the next 14 days'
    },
    {
        'days': 30,
        'label': 'In the next month',
        'subtitle': 'Show tasks that are due in the next 30 days'
    },
    {
        'days': 90,
        'label': 'In the next 3 months',
        'subtitle': 'Show tasks that are due in the next 90 days'
    }
]


def _default_label(days):
    return 'In the next %d day%s' % (days, '' if days == 1 else 's')


def _duration_info(days):
    duration_info = [d for d in _durations if d['days'] == days]

    if len(duration_info) > 0:
        return duration_info[0]
    else:
        return {
            'days': days,
            'label': _default_label(days),
            'subtitle': 'Your custom duration',
            'custom': True
        }


def filter(args):
    wf = workflow()
    prefs = Preferences.current_prefs()
    command = args[1] if len(args) > 1 else None
    duration_info = _duration_info(prefs.upcoming_duration)

    if command == 'duration':
        selected_duration = prefs.upcoming_duration

        # Apply selected duration option
        if len(args) > 2:
            try:
                selected_duration = int(args[2])
            except:
                pass

        duration_info = _duration_info(selected_duration)

        if 'custom' in duration_info:
            wf.add_item(duration_info['label'], duration_info['subtitle'], arg='-upcoming duration %d' % (duration_info['days']), valid=True, icon=icons.RADIO_SELECTED if duration_info['days'] == selected_duration else icons.RADIO)

        for duration_info in _durations:
            wf.add_item(duration_info['label'], duration_info['subtitle'], arg='-upcoming duration %d' % (duration_info['days']), valid=True, icon=icons.RADIO_SELECTED if duration_info['days'] == selected_duration else icons.RADIO)

        wf.add_item('Back', autocomplete='-upcoming ', icon=icons.BACK)

        return

    # Force a sync if not done recently or join if already running
    if datetime.now() - prefs.last_sync > timedelta(seconds=30) or is_running('sync'):
        sync()

    wf.add_item(duration_info['label'], subtitle='Change the duration for upcoming tasks', autocomplete='-upcoming duration ', icon=icons.UPCOMING)

    conditions = True

    # Build task title query based on the args
    for arg in args[1:]:
        if len(arg) > 1:
            conditions = conditions & (Task.title.contains(arg) | List.title.contains(arg))

    if conditions is None:
        conditions = True

    tasks = Task.select().join(List).where(
        Task.completed_at.is_null() &
        (Task.due_date < date.today() + timedelta(days=duration_info['days'] + 1)) &
        (Task.due_date > date.today() + timedelta(days=1)) &
        Task.list.is_null(False) &
        conditions
    )\
        .join(Reminder, JOIN.LEFT_OUTER)\
        .order_by(Task.due_date.asc(), Reminder.date.asc(), Task.order.asc())

    try:
        for t in tasks:
            wf.add_item(u'%s – %s' % (t.list_title, t.title), t.subtitle(), autocomplete='-task %s ' % t.id, icon=icons.TASK_COMPLETED if t.completed else icons.TASK)
    except OperationalError:
        background_sync()

    wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

    # Make sure tasks stay up-to-date
    background_sync_if_necessary(seconds=2)

def commit(args, modifier=None):
    relaunch_alfred = False
    prefs = Preferences.current_prefs()
    action = args[1]

    if action == 'duration':
        relaunch_alfred = True
        prefs.upcoming_duration = int(args[2])

    if relaunch_alfred:
        import subprocess
        subprocess.call(['/usr/bin/env', 'osascript', 'bin/launch_alfred.scpt', 'wl-upcoming '])
