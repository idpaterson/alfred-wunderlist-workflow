from wunderlist.api import lists
from wunderlist import util

def _list_name(args):
	return ' '.join(args[2:])

def filter(args):
	if 'create' in args:
		list_name = _list_name(args)
		subtitle = list_name if list_name else 'Type the name of the list'

		util.workflow().add_item('Create a list', subtitle, arg=' '.join(args), valid=True)
	else:
		for list in lists.lists():
				util.workflow().add_item(list['title'])

def commit(args):
	if 'create' in args:
		list_name = _list_name(args)

		lists.create_list(list_name)