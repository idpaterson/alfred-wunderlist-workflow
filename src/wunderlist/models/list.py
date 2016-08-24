import logging
import time

from peewee import (BooleanField, CharField, IntegerField, PeeweeException,
                    PrimaryKeyField, TextField)

from wunderlist.models.fields import DateTimeUTCField
from wunderlist.models.base import BaseModel
from wunderlist.util import workflow, NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


class List(BaseModel):
    id = PrimaryKeyField()
    title = TextField(index=True)
    list_type = CharField()
    public = BooleanField()
    completed_count = IntegerField(default=0)
    uncompleted_count = IntegerField(default=0)
    order = IntegerField(index=True)
    revision = IntegerField()
    created_at = DateTimeUTCField()

    @classmethod
    def sync(cls):
        from wunderlist.api import lists
        start = time.time()

        lists_data = lists.lists()
        instances = []

        log.info('Retrieved all %d lists in %s', len(lists_data), time.time() - start)
        start = time.time()

        workflow().store_data('lists', lists_data)

        try:
            instances = cls.select(cls.id, cls.revision, cls.title)
        except PeeweeException:
            pass

        log.info('Loaded all %d lists from the database in %s', len(instances), time.time() - start)

        return cls._perform_updates(instances, lists_data)

    @classmethod
    def _populate_api_extras(cls, info):
        from wunderlist.api.lists import update_list_with_tasks_count

        update_list_with_tasks_count(info)

        return info

    def __str__(self):
        return u'<%s %d %s>' % (type(self).__name__, self.id, self.title)

    def _sync_children(self):
        from wunderlist.models.task import Task

        Task.sync_tasks_in_list(self)

    class Meta:
        order_by = ('order', 'id')
        has_children = True
