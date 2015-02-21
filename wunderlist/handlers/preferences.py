from wunderlist.models.user import User
from wunderlist.util import workflow

def filter(args):
	current_user = User.get()

	workflow().add_item(
		'Sign out',
		'You are logged in as ' + current_user.name,
		autocomplete='logout'
	)

	workflow().add_item(
		'Force Sync',
		'The workflow syncs automatically, but feel free to be forcible.',
		arg='sync', valid=True
	)

def commit(args):
	if 'sync' in args:
		from wunderlist.sync import sync
		sync()