from wunderlist import util, icons

def _list_name(args):
	return ' '.join(args[1:]).strip()

def filter(args):
	list_name = _list_name(args)
	subtitle = list_name if list_name else 'Type the name of the list'

	util.workflow().add_item('New list...', subtitle, arg='--stored-query', valid=list_name != '', icon=icons.LIST_NEW)

	util.workflow().add_item(
		'Main menu',
		autocomplete='', icon=icons.BACK
	)

def commit(args, modifier=None):
	from wunderlist.api import lists
	from wunderlist.sync import backgroundSync

	list_name = _list_name(args)

	lists.create_list(list_name)

	print 'The new list was created'

	backgroundSync()