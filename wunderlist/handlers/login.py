from wunderlist import util, auth, icons

def filter(args):
	util.workflow().add_item(
		'Please log in',
		'Authorize Alfred Wunderlist Workflow to use your Wunderlist account',
		valid=True,
		icon=icons.ACCOUNT
	)

def commit(args):
	auth.authorize()