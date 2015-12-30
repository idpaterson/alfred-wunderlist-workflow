from peewee import Model, SqliteDatabase, ForeignKeyField, DateField, DateTimeField, TimeField
from wunderlist.util import workflow
from copy import copy
import dateutil

db = SqliteDatabase(workflow().datadir + '/wunderlist.db', threadlocals=True)

class BaseModel(Model):

	@classmethod
	def _api2model(cls, data):
		fields = copy(cls._meta.fields)

		# Map relationships, e.g. from user_id to user
		for (k,v) in cls._meta.fields.iteritems():
			if k.endswith('_id'):
				fields[k[:-3]] = v
			elif isinstance(v, ForeignKeyField):
				fields[k + '_id'] = v
			elif isinstance(v, (DateTimeField, DateField, TimeField)) and isinstance(fields[k], basestring):
				fields[k] = dateutil.parse(v)

		# Map each data property to the correct field
		return {fields[k].name : v for (k,v) in data.iteritems() if k in fields}

	@classmethod
	def sync(cls):
		pass

	@classmethod
	def _perform_updates(cls, model_instances, update_items):
		from concurrent import futures

		# Map of id to the normalized item
		update_items = { item['id']:cls._api2model(item) for item in update_items }
		all_instances = []

		with futures.ThreadPoolExecutor(max_workers=4) as executor:
			with db.transaction():
				for instance in model_instances:
					if not instance:
						continue
					if instance.id in update_items:
						update_item = update_items[instance.id]
						all_instances.append(instance)

						# If the revision is different, sync any children, then update the db
						if instance.revision != update_item['revision']:
							executor.submit(instance._sync_children)
							cls.update(**update_item).where(cls.id == instance.id).execute()

						del update_items[instance.id]
					# The model does not exist anymore
					else:
						instance.delete_instance()

				for update_item in update_items.values():
					instance = cls.create(**update_item)
					executor.submit(instance._sync_children)
					all_instances.append(instance)

		return all_instances

	@classmethod
	def _populate_api_extras(cls, info):
		return info

	def _sync_children(self):
		pass

	class Meta:
		database = db