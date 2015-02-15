from wunderlist import util, auth

def filter(args):
	util.workflow().add_item(
		'Are you sure?',
		'You will need to log in to a Wunderlist account to continue using the workflow',
		arg=' '.join(args),
		valid=True
	)

def commit(args):
	auth.deauthorize()