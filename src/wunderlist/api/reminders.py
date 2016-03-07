from requests import codes
from dateutil.tz import tzlocal
import wunderlist.api.base as api

NO_CHANGE = '!nochange!'

def reminders(list_id=None, task_id=None, completed=False):
    data = {
        'completed': completed
    }
    if list_id:
        data['list_id'] = int(list_id)
    elif task_id:
        data['task_id'] = int(task_id)
    req = api.get('reminders', data)
    reminders = req.json()

    return reminders

def reminder(id):
    req = api.get('reminders/' + id)
    info = req.json()

    return info

def create_reminder(task_id, date=None):
    date = date.replace(tzinfo=tzlocal())

    params = {
        'task_id': int(task_id),
        'date': date.isoformat()
    }

    req = api.post('reminders', params)
    info = req.json()

    return info

def update_reminder(id, revision, date=NO_CHANGE):
    params = {
        'revision': revision
    }

    if date != NO_CHANGE:
        if date:
            date = date.replace(tzinfo=tzlocal())
            params['date'] = date.isoformat()
        else:
            params['date'] = null

    req = api.patch('reminders/' + id, params)
    info = req.json()

    return info

def delete_task(id, revision):
    req = api.delete('reminders/' + id, {'revision': revision})

    return req.status_code == codes.no_content
