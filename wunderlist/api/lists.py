import requests
import wunderlist.api.base as api

SMART_LISTS = [
	'inbox'
]

def lists(order='display'):
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
		info['task_counts'] = list_tasks_count(id)

	return info

def list_tasks_count(id):
	req = api.get('lists/tasks_count', { 'list_id': id })
	info = req.json()

	return info

def create_list(title):
	req = api.post('lists', { 'title': title })
	info = req.json()

	return info

def delete_list(id, revision):
	req = api.delete('lists/' + id, { 'revision': revision })
	
	return req.status_code == requests.codes.no_content 