import re

from peewee import CharField, IntegerField

from wunderlist.models.base import BaseModel

_hashtag_pattern = r'(?<=\s)#\S+'

# Remove any non-word characters at the end of the hashtag
_hashtag_trim_pattern = r'\W+$'

class Hashtag(BaseModel):
    id = CharField(primary_key=True)
    revision = IntegerField(default=0)

    @classmethod
    def sync(cls):
        from wunderlist.models.task import Task

        tasks_with_hashtags = Task.select().where(Task.title.contains('#'))
        hashtags = set()

        for task in tasks_with_hashtags:
            hashtags.update(cls.hashtags_in_task(task))

        if len(hashtags) > 0:
            hashtag_data = [{'id': re.sub(_hashtag_trim_pattern, r'', tag, flags=re.UNICODE)} for tag in hashtags]
            instances = cls.select()

            cls._perform_updates(instances, hashtag_data)

    @classmethod
    def hashtags_in_task(cls, task):
        return set(re.findall(_hashtag_pattern, ' ' + task.title))
