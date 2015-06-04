from peewee import Model, SqliteDatabase
from wunderlist.util import workflow

db = SqliteDatabase(workflow().datadir + '/wunderlist.db', threadlocals=True)

class BaseModel(Model):

	@classmethod
	def _api2model(cls, data):
		fields = cls._meta.fields

		# Map relationships, e.g. from user_id to user
		for (k,v) in fields.iteritems():
			if k.endswith('_id'):
				fields[k[:-3]] = v

		return {k:v for (k,v) in data.iteritems() if k in fields}

	@classmethod
	def sync(cls):
		pass

	@classmethod
	def _perform_updates(cls, model_instances, update_items):
		# Map of id to the normalized item
		update_items = { item['id']:cls._api2model(item) for item in update_items }

		for instance in model_instances:
			if not instance:
				continue
			if instance.id in update_items:
				update_item = update_items[instance.id]

				# If the revision is different, sync any children, then update the db
				if instance.revision != update_item['revision']:
					instance._sync_children()
					cls.update(**update_item).where(cls.id == instance.id).execute()

				del update_items[instance.id]
			# The model does not exist anymore
			else:
				instance.delete_instance()

		for update_item in update_items.values():
			instance = cls.create(**update_item)
			instance._sync_children()

	@classmethod
	def _populate_api_extras(cls, info):
		return info

	def _sync_children(self):
		pass

	class Meta:
		database = db