from peewee import (ForeignKeyField, IntegerField, PeeweeException,
                    PrimaryKeyField)

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

        cls._perform_updates([instance], [root.root()], threading=False)

        return None

    def _sync_children(self):
        from concurrent import futures

        lists_data = List.prepare_sync_data()

        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(_sync_user),
            executor.submit(_sync_lists, lists_data),
            executor.submit(_sync_preferences)

        # Wait until all tasks are synced before syncing reminders and
        # hashtags since these are dependent on tasks.
        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(_sync_reminders),
            executor.submit(_sync_hashtags)

def _sync_user():
    User.sync()

def _sync_lists(lists_data):
    List.sync(lists_data)

def _sync_preferences():
    from wunderlist.models.preferences import Preferences

    Preferences.sync()

def _sync_reminders():
    from wunderlist.models.reminder import Reminder

    Reminder.sync()

def _sync_hashtags():
    from wunderlist.models.hashtag import Hashtag

    Hashtag.sync()
