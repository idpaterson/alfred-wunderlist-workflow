from wunderlist.util import workflow
from wunderlist.sync import backgroundSync

def filter(args):
	workflow().add_item(
		'New task',
		'Begin typing to add a new task',
		autocomplete=':'
	)

	workflow().add_item(
		'New list',
		autocomplete='new list '
	)

	workflow().add_item(
		'Preferences',
		autocomplete='pref '
	)

	backgroundSync()