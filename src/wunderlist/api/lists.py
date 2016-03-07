from requests import codes
import wunderlist.api.base as api

SMART_LISTS = [
    'inbox'
]

def lists(order='display', task_counts=False):
    req = api.get('lists')
    lists = req.json()

    if order == 'display':
        positions = list_positions()

        def position(list):
            if list['list_type'] in SMART_LISTS:
                return SMART_LISTS.index(list['list_type'])
            elif list['id'] in positions:
                return positions.index(list['id']) + len(SMART_LISTS)
            else:
                return list['id']

        lists.sort(key=position)

    if task_counts:
        for list in lists:
            update_list_with_tasks_count(list)

    for (index, list) in enumerate(lists):
        if list['list_type'] in SMART_LISTS:
            # List is not capitalized
            list[u'title'] = list['title'].title()
        list[u'order'] = index

    return lists

def list_positions():
    req = api.get('list_positions')
    info = req.json()

    return info[0]['values']

def list(id, task_counts=False):
    req = api.get('lists/' + id)
    info = req.json()

    # TODO: run this request in parallel
    if task_counts:
        _update_list_with_tasks_count(info)

    return info

def list_tasks_count(id):
    req = api.get('lists/tasks_count', {'list_id': id})
    info = req.json()

    return info

def update_list_with_tasks_count(info):
    counts = list_tasks_count(info['id'])

    info['completed_count'] = counts['completed_count'] if 'completed_count' in counts else 0
    info['uncompleted_count'] = counts['uncompleted_count'] if 'uncompleted_count' in counts else 0

    return info

def create_list(title):
    req = api.post('lists', {'title': title})
    info = req.json()

    return info

def delete_list(id, revision):
    req = api.delete('lists/' + id, {'revision': revision})

    return req.status_code == codes.no_content
