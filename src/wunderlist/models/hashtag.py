import re
from peewee import *
from wunderlist.models.base import BaseModel

_hashtag_pattern = r'(?<=\s)#\S+'

# Remove any non-word characters at the end of the hashtag
_hashtag_trim_pattern = r'\W+$'

class Hashtag(BaseModel):
	id = CharField(primary_key=True)

	@classmethod
	def sync(cls):
		from task import Task

		tasks_with_hashtags = Task.select().where(Task.title.contains('#'))
		hashtags = set()

		for task in tasks_with_hashtags:
			hashtags.update(cls.hashtags_in_task(task))

		if len(hashtags) > 0:
			hashtag_data = [{'id': re.sub(_hashtag_trim_pattern, r'', tag, flags=re.UNICODE)} for tag in hashtags]
			instances = cls.select()

			cls._perform_updates(instances, hashtag_data)

	@classmethod
	def sync_hashtags_in_task(cls, task):
		hashtags = cls.hashtags_in_task(task)

		if len(hashtags) > 0:
			hashtag_data = [{'id': re.sub(_hashtag_trim_pattern, r'', tag, flags=re.UNICODE)} for tag in hashtags]

			cls.insert_many(hashtag_data).upsert(True).execute()

	@classmethod
	def hashtags_in_task(cls, task):
		return set(re.findall(_hashtag_pattern, ' ' + task.title))
