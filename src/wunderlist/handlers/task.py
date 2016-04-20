# encoding: utf-8

from datetime import date

from wunderlist import icons
from wunderlist.models.task import Task
from wunderlist.models.task_parser import TaskParser
from wunderlist.util import workflow

_star = u'★'
_recurrence = u'↻'
_reminder = u'⏰'

def _task(args):
    return TaskParser(' '.join(args))

def filter(args):
    task_id = args[1]
    wf = workflow()
    matching_hashtags = []
    task = None

    try:
        task = Task.get(Task.id == task_id)
    except Task.DoesNotExist:
        pass

    if not task:
        wf.add_item('Unknown task', 'The ID does not match a task', autocomplete='', icon=icons.BACK)
    else:
        subtitle = task.subtitle()

        if task.completed:
            wf.add_item('Mark task not completed', subtitle, modifier_subtitles={
            }, arg=' '.join(args + ['toggle-completion']), valid=True, icon=icons.TASK_COMPLETED)
        else:
            wf.add_item('Complete this task', subtitle, modifier_subtitles={
                'alt': u'…and set due today    %s' % subtitle
            }, arg=' '.join(args + ['toggle-completion']), valid=True, icon=icons.TASK)

        if task.recurrence_type and not task.completed:
            wf.add_item('Delete', 'Delete this task and cancel recurrence', arg=' '.join(args + ['delete']), valid=True, icon=icons.TRASH)
        else:
            wf.add_item('Delete', 'Delete this task', arg=' '.join(args + ['delete']), valid=True, icon=icons.TRASH)

        wf.add_item('Let\'s discuss this screen', 'What task-level features do you need here?', arg=' '.join(args + ['discuss']), valid=True, icon=icons.DISCUSS)

        wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args, modifier=None):
    from wunderlist.api import tasks
    from wunderlist.sync import background_sync

    task_id = args[1]
    action = args[2]
    task = Task.get(Task.id == task_id)

    if action == 'toggle-completion':
        due_date = task.due_date

        if modifier == 'alt':
            due_date = date.today()

        if task.completed:
            tasks.update_task(task.id, task.revision, completed=False, due_date=due_date)
            print 'The task was marked incomplete'
        else:
            tasks.update_task(task.id, task.revision, completed=True, due_date=due_date)
            print 'The task was marked complete'

    elif action == 'delete':
        if tasks.delete_task(task.id, task.revision):
            print 'The task was deleted'
        else:
            print 'Please try again'

    elif action == 'discuss':
        import webbrowser

        webbrowser.open('https://github.com/idpaterson/alfred-wunderlist-workflow/issues/94')

    background_sync(True)
