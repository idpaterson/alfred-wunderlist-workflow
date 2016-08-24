from copy import copy
import logging
import time

from dateutil import parser
from peewee import (DateField, DateTimeField, ForeignKeyField, Model,
                    SqliteDatabase, TimeField)

from wunderlist.util import workflow, NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())

db = SqliteDatabase(workflow().datadir + '/wunderlist.db', threadlocals=True)

def _balance_keys_for_insert(values):
    all_keys = set()
    for v in values:
        all_keys.update(v)

    balanced_values = []
    for v in values:
        balanced = {}
        for k in all_keys:
            balanced[k] = v.get(k)
        balanced_values.append(balanced)

    return balanced_values

class BaseModel(Model):

    @classmethod
    def _api2model(cls, data):
        fields = copy(cls._meta.fields)
        model_data = {}

        # Map relationships, e.g. from user_id to user's
        for (field_name, field) in cls._meta.fields.iteritems():
            if field_name.endswith('_id'):
                fields[field_name[:-3]] = field
            elif isinstance(field, ForeignKeyField):
                fields[field_name + '_id'] = field

            # The Wunderlist API does not include some falsy values. For
            # example, if a task is completed then marked incomplete the
            # updated data will not include a completed key, so we have to set
            # the defaults for everything that is not specified
            if field.default:
                model_data[field_name] = field.default
            elif field.null:
                model_data[field_name] = None

        # Map each data property to the correct field
        for (k, v) in data.iteritems():
            if k in fields:
                if isinstance(fields[k], (DateTimeField, DateField, TimeField)):
                    model_data[fields[k].name] = parser.parse(v)
                else:
                    model_data[fields[k].name] = v

        return model_data

    @classmethod
    def sync(cls):
        pass

    @classmethod
    def _perform_updates(cls, model_instances, update_items):
        start = time.time()
        instances_by_id = dict((instance.id, instance) for instance in model_instances if instance)

        # Remove all update metadata and instances that have the same revision
        # before any additional processing on the metadata
        def revised(item):
            id = item['id']
            if id in instances_by_id and instances_by_id[id].revision == item['revision']:
                instance = instances_by_id[id]
                del instances_by_id[id]

                logger = log.debug

                if type(instance)._meta.expect_revisions:
                    logger = log.info

                logger('Revision %d of %s is still the latest', instance.revision, instance)

                return False
            return True

        changed_items = [item for item in update_items if revised(item)]

        # Map of id to the normalized item
        changed_items = dict((item['id'], cls._api2model(item)) for item in changed_items)
        all_instances = []
        log.info('Prepared %d of %d updated items in %s', len(changed_items), len(update_items), time.time() - start)

        # Update all the changed metadata and remove instances that no longer
        # exist
        with db.atomic():
            for id, instance in instances_by_id.iteritems():
                if not instance:
                    continue
                if id in changed_items:
                    changed_item = changed_items[id]
                    all_instances.append(instance)

                    if cls._meta.has_children:
                        log.info('Syncing children of %s', instance)
                        instance._sync_children()
                    cls.update(**changed_item).where(cls.id == id).execute()
                    log.info('Updated %s to revision %d', instance, changed_item['revision'])
                    log.debug('with data %s', changed_item)

                    del changed_items[id]
                # The model does not exist anymore
                else:
                    instance.delete_instance()
                    log.info('Deleted %s', instance)

        # Bulk insert and retrieve
        new_values = changed_items.values()

        # Insert in batches
        for i in xrange(0, len(new_values), 500):
            inserted_chunk = _balance_keys_for_insert(new_values[i:i + 500])

            with db.atomic():
                cls.insert_many(inserted_chunk).execute()

                log.info('Created %d of model %s', len(inserted_chunk), cls.__name__)

                inserted_ids = [i['id'] for i in inserted_chunk]
                inserted_instances = cls.select().where(cls.id.in_(inserted_ids))

                for instance in inserted_instances:
                    if type(instance)._meta.has_children:
                        log.info('Syncing children of %s', instance)
                        instance._sync_children()

                all_instances += inserted_instances

        return all_instances

    @classmethod
    def _populate_api_extras(cls, info):
        return info

    def __str__(self):
        return '<%s %s>' % (type(self).__name__, self.id)

    def _sync_children(self):
        pass

    class Meta(object):
        database = db
        expect_revisions = False
        has_children = False
