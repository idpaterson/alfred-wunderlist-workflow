from wunderlist.util import workflow

_icon_theme = None

def alfred_is_dark():
	# Formatted rgba(255,255,255,0.90)
	background_rgba = workflow().alfred_env['theme_background']
	if background_rgba:
		rgb = [int(x) for x in background_rgba[5:-6].split(',')]
		return (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255 < 0.5
	return False

def icon_theme():
	global _icon_theme
	if not _icon_theme:
		prefs = workflow().stored_data('prefs')

		if prefs and 'icon_theme' in prefs:
			_icon_theme = prefs['icon_theme']
		else:
			_icon_theme = 'light' if alfred_is_dark() else 'dark'

	return _icon_theme

_icon_path = 'icons/%s/' % icon_theme()

ACCOUNT = _icon_path + 'account.png'
BACK = _icon_path + 'back.png'
CALENDAR = _icon_path + 'calendar.png'
CANCEL = _icon_path + 'cancel.png'
CHECKMARK = _icon_path + 'checkmark.png'
DOWNLOAD = _icon_path + 'download.png'
HELP = _icon_path + 'help.png'
INBOX = _icon_path + 'inbox.png'
INFO = _icon_path + 'info.png'
LIST = _icon_path + 'list.png'
LIST_NEW = _icon_path + 'list_new.png'
NEXT_WEEK = _icon_path + 'next_week.png'
PAINTBRUSH = _icon_path + 'paintbrush.png'
PREFERENCES = _icon_path + 'preferences.png'
RECURRENCE = _icon_path + 'recurrence.png'
REMINDER = _icon_path + 'reminder.png'
STAR = _icon_path + 'star.png'
STAR_REMOVE = _icon_path + 'star_remove.png'
SYNC = _icon_path + 'sync.png'
TASK = _icon_path + 'task.png'
TASK_COMPLETED = _icon_path + 'task_completed.png'
TODAY = _icon_path + 'today.png'
TOMORROW = _icon_path + 'tomorrow.png'
