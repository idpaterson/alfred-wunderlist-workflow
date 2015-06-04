from peewee import *
from wunderlist.models.base import BaseModel
from wunderlist.models.list import List
from wunderlist.models.user import User

class Task(BaseModel):
	id = PrimaryKeyField()
	list_id = ForeignKeyField(List, related_name='tasks')
	title = CharField(index=True)
	completed_at = DateTimeField()
	completed_by_id = ForeignKeyField(User, related_name='completed_tasks')
	starred = BooleanField(index=True)
	due_date = DateField(index=True)
	assignee_id = ForeignKeyField(User, related_name='assigned_tasks')
	order = IntegerField(index=True)
	revision = IntegerField()
	created_at = DateTimeField()
	created_by_id = ForeignKeyField(User, related_name='created_tasks')

	class Meta:
		order_by = ('order', 'id')