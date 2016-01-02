# encoding: utf-8

from wunderlist import auth, icons
from wunderlist.util import workflow
import re

def filter(args):
	started_auth = workflow().stored_data('auth')
	getting_help = len(args) > 1

	if not getting_help:
		workflow().add_item(
			'Please log in',
			'Authorize Alfred Wunderlist Workflow to use your Wunderlist account',
			valid=True, icon=icons.ACCOUNT
		)

	# If the auth process has started, allow user to paste a key manually
	if started_auth:
		if getting_help:
			workflow().add_item(
				'A "localhost" page appeared in my web browser',
				u'Paste the full link from your browser into Alfred then press return, wl http://localhost:6200/…',
				arg=' '.join(args), valid=True, icon=icons.LINK
			)
			workflow().add_item(
				'Other issues?',
				'See outstanding issues and report your own bugs or feedback',
				arg=':about issues', valid=True, icon=icons.HELP
			)
		else:
			workflow().add_item(
				'Having trouble?',
				'Did you see an error after logging in to Wunderlist?',
				autocomplete=' ', valid=False, icon=icons.HELP
			)

	if not getting_help:
		workflow().add_item(
			'About',
			'Learn about the workflow and get support',
			autocomplete=':about ',
			icon=icons.INFO
		)

def commit(args):
	started_auth = workflow().stored_data('auth')
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
