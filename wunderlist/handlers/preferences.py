from wunderlist.api.user import user
from wunderlist.util import workflow

def filter(args):
	current_user = user()

	workflow().add_item(
		'Sign out',
		'You are logged in as ' + current_user['name'],
		autocomplete='logout'
	)