from peewee import IntegerField, PeeweeException, PrimaryKeyField, TextField

from wunderlist.models import DateTimeUTCField
from wunderlist.models.base import BaseModel


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
        except User.DoesNotExist:
            pass

        cls._perform_updates([instance], [user.user()])

        return None
