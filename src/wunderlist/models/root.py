import logging
import time

from peewee import ForeignKeyField, IntegerField, PrimaryKeyField
from workflow.notify import notify

from wunderlist.models.base import BaseModel
from wunderlist.models.list import List
from wunderlist.models.user import User
from wunderlist.util import NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


class Root(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, null=True)
    revision = IntegerField()

    @classmethod
    def sync(cls, background=False):
        from wunderlist.api import root

        start = time.time()
        instance = None
        root_data = root.root()

        log.info('Retrieved Root revision in %s', time.time() - start)

        try:
            instance = cls.get()
        except Root.DoesNotExist:
            pass

        if not background and instance.revision != root_data['revision']:
            notify('Please wait...', 'The workflow is making sure your tasks are up-to-date')

        return cls._perform_updates([instance], [root_data])

    def _sync_children(self):
        from wunderlist.models.hashtag import Hashtag
        from wunderlist.models.preferences import Preferences
        from wunderlist.models.reminder import Reminder

        start = time.time()
        user_revised = User.sync()
        log.info('Synced user in %s', time.time() - start)
        start = time.time()

        lists_revised = List.sync()
        log.info('Synced lists and tasks in %s', time.time() - start)
        start = time.time()

        # Changes to reminders or settings increment the User revision
        if user_revised:
            Preferences.sync()
            log.info('Synced preferences in %s', time.time() - start)
            start = time.time()

            Reminder.sync()
            log.info('Synced reminders in %s', time.time() - start)
            start = time.time()

        # Changes in lists or tasks require hashtags to be updated
        if lists_revised:
            Hashtag.sync()
            log.info('Synced hashtags in %s', time.time() - start)

    def __str__(self):
        return '<%s>' % (type(self).__name__)

    class Meta(object):
        expect_revisions = True
        has_children = True
