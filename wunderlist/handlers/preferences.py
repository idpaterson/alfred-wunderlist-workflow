from wunderlist.models.user import User
from wunderlist.util import workflow
from wunderlist import icons

def filter(args):
	current_user = User.get()

	workflow().add_item(
		'Sign out',
		'You are logged in as ' + current_user.name,
		autocomplete='logout', icon=icons.CANCEL
	)

	workflow().add_item(
		'Switch theme',
		'Toggle between light and dark icons',
		arg='pref retheme',
		valid=True,
		icon=icons.PAINTBRUSH
	)

	workflow().add_item(
		'Force Sync',
		'The workflow syncs automatically, but feel free to be forcible.',
		arg='sync', valid=True, icon=icons.SYNC
	)

	workflow().add_item(
		'Main menu',
		autocomplete='', icon=icons.BACK
	)

def commit(args):
	if 'sync' in args:
		from wunderlist.sync import sync
		sync()
	elif 'retheme' in args:
		import subprocess

		prefs = workflow().stored_data('prefs')
		if not prefs:
			prefs = { 'icon_theme': 'dark' }

		prefs['icon_theme'] = 'light' if prefs['icon_theme'] == 'dark' else 'dark'

		workflow().store_data('prefs', prefs)

		subprocess.call(['/usr/bin/env', 'osascript', 'launch_alfred.scpt', 'wl pref'])