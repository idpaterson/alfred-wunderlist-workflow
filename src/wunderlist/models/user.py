from peewee import *
from base import BaseModel
from wunderlist.models import DateTimeUTCField

class User(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    revision = IntegerField()
    created_at = DateTimeUTCField()

    @classmethod
    def sync(cls):
        from wunderlist.api import user

        instance = None

        try:
            instance = cls.get()
        except:
            pass

        cls._perform_updates([instance], [user.user()])

        return None
