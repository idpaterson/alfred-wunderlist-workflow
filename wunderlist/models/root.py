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

	def _sync_children(self):
		from list import List

		List.sync()
		User.sync()