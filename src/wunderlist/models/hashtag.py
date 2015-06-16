import re
from peewee import *
from wunderlist.models.base import BaseModel

# Wunderlist includes any and all non-whitespace characters in a hashtag,
# requiring only that the hash be preceded by a space or come at the beginning
# of a string
_hashtag_pattern = r'(?<=\s)#\S+'
_hashtag_pattern_bos = r'^#\S+'

class Hashtag(BaseModel):
	id = PrimaryKeyField()
	tag = CharField(unique=True)

	@classmethod
	def sync_hashtags_in_task(cls, task):
		hashtags = set(re.findall(_hashtag_pattern, task.title) + re.findall(_hashtag_pattern_bos, task.title))

		if len(hashtags) > 0:
			hashtag_data = [{u'tag': tag} for tag in hashtags]

			print cls.insert_many(hashtag_data).upsert(upsert=True)

			cls.insert_many(hashtag_data).upsert(True).execute()
