from peewee import PrimaryKeyField, ForeignKeyField, IntegerField, DateTimeField
from base import BaseModel
from wunderlist.models.task import Task

class Reminder(BaseModel):
	id = PrimaryKeyField()
	task = ForeignKeyField(Task, null=True, related_name='reminders')
	# FIXME: Something is causing peewee to store reminder dates in a format
	# that is not supported for reading dates by default (%z +0000 suffix)
	date = DateTimeField(formats=('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f%z'))
	revision = IntegerField()
	created_at = DateTimeField(formats=('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S.%f%z'))

	@classmethod
	def sync(cls):
		from wunderlist.api import reminders

		instances = []

		try:
			instances = cls.select()
		except:
			pass

		reminders_data = reminders.reminders()

		cls._perform_updates(instances, reminders_data)
