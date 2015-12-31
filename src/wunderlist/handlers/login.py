from wunderlist import util, auth, icons
import re

def filter(args):
	workflow = util.workflow()
	started_auth = workflow.stored_data('auth')
	manual_verification_url = re.search(r'http://\S+', ' '.join(args))

	if not (started_auth and manual_verification_url):
		workflow.add_item(
			'Please log in',
			'Authorize Alfred Wunderlist Workflow to use your Wunderlist account',
			valid=True,
			icon=icons.ACCOUNT
		)

	# If the auth process has started, allow user to paste a key manually
	if started_auth:
		workflow.add_item(
			'Having trouble?',
			'Paste the full http://localhost:6200 URL from your browser then press the return key to continue',
			autocomplete=None if manual_verification_url else ' http://localhost:6200/?',
			arg=manual_verification_url.group() if manual_verification_url else None,
			valid=manual_verification_url,
			icon=icons.HELP
		)

def commit(args):
	workflow = util.workflow()
	started_auth = workflow.stored_data('auth')
	manual_verification_url = re.search(r'http://\S+', ' '.join(args))

	if started_auth and manual_verification_url:
		auth_status = auth.handle_authorization_url(manual_verification_url.group())

		if auth_status is True:
			# Reopen the workflow
			import subprocess
			subprocess.call(['/usr/bin/env', 'osascript', 'bin/launch_alfred.scpt', 'wl'])
		elif not auth_status:
			print 'Invalid or expired URL, please try again'
	else:
		auth.authorize()
