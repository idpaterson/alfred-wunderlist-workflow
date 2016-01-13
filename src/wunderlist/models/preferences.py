from datetime import time, timedelta
from wunderlist.util import workflow

REMINDER_TIME_KEY = 'reminder_time'
ICON_THEME_KEY = 'icon_theme'
EXPLICIT_KEYWORDS_KEY = 'explicit_keywords'
AUTOMATIC_REMINDERS_KEY = 'automatic_reminders'
REMINDER_TODAY_OFFSET_KEY = 'reminder_today_offset'
LAST_SYNC_KEY = 'last_sync'

class Preferences(object):

	_current_prefs = None

	@classmethod
	def sync(cls):
		from wunderlist.api import settings

		prefs = cls.current_prefs()

		# Only set the default values once, otherwise allow them to be managed
		# in the workflow
		if prefs._get(AUTOMATIC_REMINDERS_KEY, None) is None:
			prefs.reminder_today_offset = time(1, 0, 0)

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
	def reminder_today_offset(self):
		return self._get(REMINDER_TODAY_OFFSET_KEY, None)

	@reminder_today_offset.setter
	def reminder_today_offset(self, reminder_today_offset):
		self._set(REMINDER_TODAY_OFFSET_KEY, reminder_today_offset)

	@property
	def reminder_today_offset_timedelta(self):
		reminder_today_offset = self.reminder_today_offset

		return timedelta(hours=reminder_today_offset.hour, minutes=reminder_today_offset.minute)

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

	@property
	def last_sync(self):
		return self._get(LAST_SYNC_KEY, None)

	@last_sync.setter
	def last_sync(self, last_sync):
		self._set(LAST_SYNC_KEY, last_sync)
