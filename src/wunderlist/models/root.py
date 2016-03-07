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
        except:
            pass

        cls._perform_updates([instance], [root.root()])

        return None

    def _sync_children(self):
        from concurrent import futures

        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(_sync_user),
            executor.submit(_sync_lists),
            executor.submit(_sync_preferences)

        List.cache_synced_lists()

        # Wait until all tasks are synced before syncing reminders and
        # hashtags since these are dependent on tasks.
        with futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(_sync_reminders),
            executor.submit(_sync_hashtags)

def _sync_user():
    User.sync()

def _sync_lists():
    List.sync()

def _sync_preferences():
    from wunderlist.models.preferences import Preferences

    Preferences.sync()

def _sync_reminders():
    from wunderlist.models.reminder import Reminder

    Reminder.sync()

def _sync_hashtags():
    from wunderlist.models.hashtag import Hashtag

    Hashtag.sync()
