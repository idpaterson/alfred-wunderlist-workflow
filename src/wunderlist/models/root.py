from peewee import *
from base import BaseModel
from user import User

class Root(BaseModel):
	id = PrimaryKeyField()
	user = ForeignKeyField(User, null=True)
	revision = IntegerField()

	@classmethod
	def sync(cls):
		from wunderlist.api import root

		instance = None

		try:
			instance = cls.get()
		except:
			pass

		cls._perform_updates([instance], [root.root()])

		return None

	def _sync_children(self):
		from concurrent import futures
		from hashtag import Hashtag

		with futures.ThreadPoolExecutor(max_workers=2) as executor:
			jobs = (
				executor.submit(_sync_user),
				executor.submit(_sync_lists),
				executor.submit(_sync_preferences),
				executor.submit(_sync_reminders)
			)

		Hashtag.sync()

def _sync_user():
	User.sync()

def _sync_lists():
	from list import List

	List.sync()

def _sync_preferences():
	from preferences import Preferences

	Preferences.sync()

def _sync_reminders():
	from reminder import Reminder

	Reminder.sync()
