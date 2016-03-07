from peewee import PrimaryKeyField, CharField, BooleanField, IntegerField, TextField
from base import BaseModel
from wunderlist.models import DateTimeUTCField
from wunderlist.util import workflow

_lists_sync_data = None

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
        global _lists_sync_data

        from wunderlist.api import lists

        instances = []

        try:
            instances = cls.select()
        except:
            pass

        lists_data = lists.lists()

        cls._perform_updates(instances, lists_data)

        _lists_sync_data = lists_data

        return None

    @classmethod
    def cache_synced_lists(cls):
        global _lists_sync_data
        workflow().store_data('lists', _lists_sync_data)

    @classmethod
    def _populate_api_extras(cls, info):
        from wunderlist.api.lists import update_list_with_tasks_count

        update_list_with_tasks_count(info)

        return info

    def _sync_children(self):
        from task import Task

        Task.sync_tasks_in_list(self)

    class Meta:
        order_by = ('order', 'id')
