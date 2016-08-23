import logging
import time

from peewee import (ForeignKeyField, IntegerField, PeeweeException,
                    PrimaryKeyField)

from wunderlist.models import DateTimeUTCField
from wunderlist.models.base import BaseModel
from wunderlist.models.task import Task
from wunderlist.util import NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


class Reminder(BaseModel):
    id = PrimaryKeyField()
    task = ForeignKeyField(Task, null=True, related_name='reminders')
    date = DateTimeUTCField()
    revision = IntegerField()
    created_at = DateTimeUTCField()

    @classmethod
    def sync(cls):
        from wunderlist.api import reminders
        start = time.time()
        instances = []

        reminders_data = reminders.reminders()

        log.info('Retrieved all %d reminders in %s', len(reminders_data), time.time() - start)
        start = time.time()

        try:
            instances = cls.select(cls.id, cls.revision)
        except PeeweeException:
            pass

        log.info('Loaded all %d reminders from the database in %s', len(instances), time.time() - start)

        return cls._perform_updates(instances, reminders_data)
