import re
from peewee import *
from wunderlist.models.base import BaseModel

_hashtag_pattern = r'(?<=\s)#\S+'
_hashtag_pattern_bos = r'^#\S+'

# Remove any non-word characters at the end of the hashtag
_hashtag_trim_pattern = r'\W+$'

class Hashtag(BaseModel):
	id = PrimaryKeyField()
	tag = CharField(unique=True)

	@classmethod
	def sync_hashtags_in_task(cls, task):
		hashtags = set(re.findall(_hashtag_pattern, task.title) + re.findall(_hashtag_pattern_bos, task.title))

		if len(hashtags) > 0:
			hashtag_data = [{'tag': re.sub(_hashtag_trim_pattern, r'', tag, flags=re.UNICODE)} for tag in hashtags]

			cls.insert_many(hashtag_data).upsert(True).execute()
