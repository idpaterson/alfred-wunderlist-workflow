import wunderlist.api.base as api


def create_note(task_id, content):
    params = {
        'task_id': int(task_id),
        'content': content
    }

    req = api.post('notes', params)
    info = req.json()

    return info
