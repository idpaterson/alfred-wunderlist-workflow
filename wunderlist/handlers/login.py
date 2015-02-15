from wunderlist import util, auth

def filter(args):
	util.workflow().add_item(
		'Please log in',
		'Authorize Alfred Wunderlist Workflow to use your Wunderlist account',
		valid=True
	)

def commit(args):
	auth.authorize()