from wunderlist import icons
from wunderlist.util import workflow


def filter(args):
    workflow().add_item(
        'New task...',
        'Begin typing to add a new task',
        autocomplete=' ',
        icon=icons.TASK_COMPLETED
    )

    workflow().add_item(
        'Due today',
        autocomplete='-due ',
        icon=icons.TODAY
    )

    workflow().add_item(
        'Find and update tasks',
        autocomplete='-search ',
        icon=icons.SEARCH
    )

    workflow().add_item(
        'New list',
        autocomplete='-list ',
        icon=icons.LIST_NEW
    )

    workflow().add_item(
        'Preferences',
        autocomplete='-pref ',
        icon=icons.PREFERENCES
    )

    workflow().add_item(
        'About',
        'Learn about the workflow and get support',
        autocomplete='-about ',
        icon=icons.INFO
    )
