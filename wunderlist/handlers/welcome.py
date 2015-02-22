from wunderlist import icons
from wunderlist.util import workflow
from wunderlist.sync import backgroundSync

def filter(args):
	workflow().add_item(
		'New task',
		'Begin typing to add a new task',
		autocomplete=':',
		icon=icons.TASK_COMPLETED
	)

	workflow().add_item(
		'New list',
		autocomplete='new list ',
		icon=icons.LIST
	)

	workflow().add_item(
		'Preferences',
		autocomplete='pref ',
		icon=icons.PREFERENCES
	)

	backgroundSync()