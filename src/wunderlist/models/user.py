from peewee import *
from base import BaseModel

class User(BaseModel):
	id = PrimaryKeyField()
	name = CharField()
	revision = IntegerField()
	created_at = DateTimeField()

	@classmethod
	def sync(cls):
		from wunderlist.api import user

		instance = None

		try:
			instance = cls.get()
		except:
			pass

		cls._perform_updates([instance], [user.user()])
