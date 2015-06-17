from peewee import *
from wunderlist.models.base import BaseModel
from wunderlist.models.list import List
from wunderlist.models.user import User

class Task(BaseModel):
	id = PrimaryKeyField()
	list = ForeignKeyField(List, related_name='tasks')
	title = CharField(index=True)
	completed_at = DateTimeField(null=True)
	completed_by = ForeignKeyField(User, related_name='completed_tasks', null=True)
	starred = BooleanField(index=True)
	due_date = DateField(index=True, null=True)
	assignee = ForeignKeyField(User, related_name='assigned_tasks', null=True)
	order = IntegerField(index=True, null=True)
	revision = IntegerField()
	created_at = DateTimeField()
	created_by = ForeignKeyField(User, related_name='created_tasks', null=True)

	@classmethod
	def sync_tasks_in_list(cls, list):
		from wunderlist.api import tasks

		instances = []

		try:
			instances = cls.select().where(cls.list == list.id)
		except:
			pass

		tasks_data = tasks.tasks(list.id, completed=False)
		tasks_data += tasks.tasks(list.id, completed=True)

		cls._perform_updates(instances, tasks_data)

	@classmethod
	def due_today(cls):
		from datetime import date

		return (cls
			.select(cls, List)
			.join(List)
			.where(cls.completed_at == None)
			.where(cls.due_date <= date.today())
			.order_by(List.order.asc(), cls.due_date.asc())
		)

	@classmethod
	def search(cls, query):
		from datetime import date

		return (cls
			.select(cls, List)
			.join(List)
			.where(cls.completed_at == None)
			.where(cls.title.contains(query))
			.order_by(List.order.asc(), cls.due_date.asc())
		)

	def _sync_children(self):
		from hashtag import Hashtag

		Hashtag.sync_hashtags_in_task(self)

	class Meta:
		order_by = ('order', 'id')
