import logging
import time

from peewee import IntegerField, PrimaryKeyField, TextField

from wunderlist.models import DateTimeUTCField
from wunderlist.models.base import BaseModel
from wunderlist.util import NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


class User(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    revision = IntegerField()
    created_at = DateTimeUTCField()

    @classmethod
    def sync(cls):
        from wunderlist.api import user

        start = time.time()
        instance = None
        user_data = user.user()
        log.info('Retrieved User in %s', time.time() - start)

        try:
            instance = cls.get()
        except User.DoesNotExist:
            pass

        return cls._perform_updates([instance], [user_data])
