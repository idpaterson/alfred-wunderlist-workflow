from peewee import PrimaryKeyField, CharField, BooleanField, IntegerField, DateTimeField
from base import BaseModel
from wunderlist.util import workflow

class List(BaseModel):
	id = PrimaryKeyField()
	title = CharField(index=True)
	list_type = CharField()
	public = BooleanField()
	completed_count = IntegerField()
	uncompleted_count  = IntegerField()
	order = IntegerField(index=True)
	revision  = IntegerField()
	created_at = DateTimeField()

	@classmethod
	def sync(cls):
		from wunderlist.api import lists

		instances = []

		try:
			instances = cls.select()
		except:
			pass

		lists_data = lists.lists()

		cls._perform_updates(instances, lists_data)

		workflow().store_data('lists', lists_data)

	@classmethod
	def _populate_api_extras(cls, info):
		lists.update_list_with_tasks_count(info)

		return info		

	def _sync_children(self):
		from task import Task

		Task.sync()

	class Meta:
		order_by = ('order', 'id')
