from requests import codes
import wunderlist.api.base as api

NO_CHANGE = '!nochange!'

def tasks(list_id, order='display', completed=False, subtasks=False, positions=None):
    req = api.get(('subtasks' if subtasks else 'tasks'), {
        'list_id': int(list_id),
        'completed': completed
    })
    tasks = req.json()

    if order == 'display':
        if positions is None:
            positions = task_positions(list_id)

        def position(task):
            try:
                return positions.index(task['id'])
            except:
                return 1e99

        tasks.sort(key=position)

    for (index, task) in enumerate(tasks):
        task[u'order'] = index

    return tasks

def task_positions(list_id):
    positions = []

    from concurrent import futures

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        jobs = (
            executor.submit(api.get, 'task_positions', {'list_id': list_id}),
            executor.submit(api.get, 'subtask_positions', {'list_id': list_id})
        )

        for job in futures.as_completed(jobs):
            req = job.result()
            data = req.json()

            if len(data) > 0:
                positions += data[0]['values']

    return positions

def task(id):
    req = api.get('tasks/%d' % int(id))
    info = req.json()

    return info

def create_task(list_id, title, assignee_id=None, recurrence_type=None, recurrence_count=None, due_date=None, reminder_date=None, starred=False, completed=False):
    params = {
        'list_id': int(list_id),
        'title': title,
        'starred': starred,
        'completed': completed
    }

    if assignee_id:
        params['assignee_id'] = int(assignee_id)

    if recurrence_type and recurrence_count:
        params['recurrence_type'] = recurrence_type
        params['recurrence_count'] = int(recurrence_count)

    if due_date:
        params['due_date'] = due_date.strftime('%Y-%m-%d')

    req = api.post('tasks', params)
    info = req.json()

    if reminder_date:
        from wunderlist.api import reminders

        reminders.create_reminder(info['id'], reminder_date)

    return info

def update_task(id, revision, title=NO_CHANGE, assignee_id=NO_CHANGE, recurrence_type=NO_CHANGE, recurrence_count=NO_CHANGE, due_date=NO_CHANGE, reminder_date=NO_CHANGE, starred=NO_CHANGE, completed=NO_CHANGE):
    params = {}
    remove = []
    changes = {
        'title': title,
        'assignee_id': assignee_id,
        'recurrence_type': recurrence_type,
        'recurrence_count': recurrence_count,
        'due_date': due_date,
        'starred': starred,
        'completed': completed
    }

    for (key, value) in changes.iteritems():
        if value is None:
            remove.append(key)
        elif value != NO_CHANGE:
            params[key] = value

    if due_date:
        params['due_date'] = due_date.strftime('%Y-%m-%d')

    if remove:
        params['remove'] = remove

    if params:
        params['revision'] = revision

        req = api.patch('tasks/%d' % int(id), params)
        info = req.json()

        return info

    return None

def delete_task(id, revision):
    req = api.delete('tasks/%d' % int(id), {'revision': revision})

    return req.status_code == codes.no_content
