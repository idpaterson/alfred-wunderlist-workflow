from peewee import PrimaryKeyField, ForeignKeyField, IntegerField, DateTimeField
from base import BaseModel
from wunderlist.models.task import Task

class Reminder(BaseModel):
	id = PrimaryKeyField()
	task = ForeignKeyField(Task, null=True, related_name='reminders')
	date = DateTimeField()
	revision = IntegerField()
	created_at = DateTimeField()

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
