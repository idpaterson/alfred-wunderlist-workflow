from peewee import *
from wunderlist.models.base import BaseModel
from wunderlist.models.list import List
from wunderlist.models.user import User

_days_by_recurrence_type = {
	'day': 1,
	'week': 7,
	'month': 30.43,
	'year': 365
}

class Task(BaseModel):
	id = PrimaryKeyField()
	list = ForeignKeyField(List, null=True, related_name='tasks')
	task = ForeignKeyField('self', null=True, related_name='subtasks')
	title = TextField(index=True)
	completed_at = DateTimeField(null=True)
	completed_by = ForeignKeyField(User, related_name='completed_tasks', null=True)
	starred = BooleanField(index=True, null=True)
	due_date = DateField(index=True, null=True)
	recurrence_type = CharField(null=True)
	recurrence_count = IntegerField(null=True)
	assignee = ForeignKeyField(User, related_name='assigned_tasks', null=True)
	order = IntegerField(index=True, null=True)
	revision = IntegerField()
	created_at = DateTimeField()
	created_by = ForeignKeyField(User, related_name='created_tasks', null=True)

	@classmethod
	def sync_tasks_in_list(cls, list):
		from wunderlist.api import tasks
		from hashtag import Hashtag
		from concurrent import futures
		instances = []
		tasks_data = []
		task_positions = tasks.task_positions(list.id)

		with futures.ThreadPoolExecutor(max_workers=4) as executor:
			jobs = (
				executor.submit(tasks.tasks, list.id, completed=False, positions=task_positions),
				executor.submit(tasks.tasks, list.id, completed=True, positions=task_positions),
				executor.submit(tasks.tasks, list.id, completed=False, subtasks=True, positions=task_positions),
				executor.submit(tasks.tasks, list.id, completed=True, subtasks=True, positions=task_positions)
			)

			for job in futures.as_completed(jobs):
				tasks_data += job.result()

		try:
			# Include all tasks thought to be in the list, plus any additional
			# tasks referenced in the data (task may have been moved to a different list)
			instances = cls.select().where(cls.task.is_null() & (cls.list == list.id) | (cls.id.in_([task['id'] for task in tasks_data])))
		except:
			pass

		all_instances = cls._perform_updates(instances, tasks_data)

		Hashtag.sync_hashtags_in_tasks(all_instances)

		return None

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

	@property
	def reminder_date(self):
		for reminder in self.reminders:
			return reminder.date
		return None

	@property
	def overdue_times(self):
		if self.recurrence_type is None:
			return 0

		from datetime import date

		recurrence_days = _days_by_recurrence_type[self.recurrence_type]
		overdue_time = date.today() - self.due_date
		return int(overdue_time.days / recurrence_days)

	@property
	def list_title(self):
		if self.list:
			return self.list.title
		return None

	class Meta:
		order_by = ('order', 'id')
