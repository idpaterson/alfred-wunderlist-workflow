from datetime import time
from wunderlist.util import workflow

REMINDER_TIME_KEY = 'reminder_time'
ICON_THEME_KEY = 'icon_theme'
EXPLICIT_KEYWORDS_KEY = 'explicit_keywords'
AUTOMATIC_REMINDERS_KEY = 'automatic_reminders'

class Preferences(object):

	_current_prefs = None

	@classmethod
	def sync(cls):
		from wunderlist.api import settings

		prefs = cls.current_prefs()

		# Only set the value once, otherwise allow it to be managed in
		# the workflow
		if prefs._get(AUTOMATIC_REMINDERS_KEY, None) is None:
			for s in settings.settings():
				if s['key'] == 'automatic_reminders':
					# In case the value, currently "on" or "off" is changed to
					# boolean this logic will still work
					prefs.automatic_reminders = s['value'] and s['value'] != 'off'
					break

	@classmethod
	def current_prefs(cls):
		if not cls._current_prefs:
			cls._current_prefs = Preferences(workflow().stored_data('prefs'))
		if not cls._current_prefs:
			cls._current_prefs = Preferences({})
		return cls._current_prefs

	def __init__(self, data):
		self._data = data or {}

	def _set(self, key, value):
		self._data[key] = value

		workflow().store_data('prefs', self._data)

	def _get(self, key, default=None, type=str):
		value = self._data.get(key)

		if value is None and default is not None:
			value = default

		return value

	@property
	def reminder_time(self):
		return self._get(REMINDER_TIME_KEY) or time(9, 0, 0)

	@reminder_time.setter
	def reminder_time(self, reminder_time):
		self._set(REMINDER_TIME_KEY, reminder_time)

	@property
	def icon_theme(self):
		return self._get(ICON_THEME_KEY)

	@icon_theme.setter
	def icon_theme(self, reminder_time):
		self._set(ICON_THEME_KEY, reminder_time)

	@property
	def explicit_keywords(self):
		return self._get(EXPLICIT_KEYWORDS_KEY, False)

	@explicit_keywords.setter
	def explicit_keywords(self, explicit_keywords):
		self._set(EXPLICIT_KEYWORDS_KEY, explicit_keywords)

	@property
	def automatic_reminders(self):
		return self._get(AUTOMATIC_REMINDERS_KEY, False)

	@automatic_reminders.setter
	def automatic_reminders(self, automatic_reminders):
		self._set(AUTOMATIC_REMINDERS_KEY, automatic_reminders)
