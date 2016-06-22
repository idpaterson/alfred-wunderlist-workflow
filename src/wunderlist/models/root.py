from peewee import ForeignKeyField, IntegerField, PrimaryKeyField

from wunderlist.models.base import BaseModel
from wunderlist.models.list import List
from wunderlist.models.user import User


class Root(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, null=True)
    revision = IntegerField()

    @classmethod
    def sync(cls):
        from wunderlist.api import root

        instance = None

        try:
            instance = cls.get()
        except Root.DoesNotExist:
            pass

        cls._perform_updates([instance], [root.root()])

        return None

    def _sync_children(self):
        from wunderlist.models.hashtag import Hashtag
        from wunderlist.models.preferences import Preferences
        from wunderlist.models.reminder import Reminder

        User.sync()
        List.sync()
        Preferences.sync()
        Reminder.sync()
        Hashtag.sync()

    def __str__(self):
        return '<%s>' % (type(self).__name__)

    class Meta:
        expect_revisions = True
        has_children = True
