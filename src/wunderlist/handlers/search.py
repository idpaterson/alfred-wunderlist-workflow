# encoding: utf-8

import re

from workflow import MATCH_ALL, MATCH_ALLCHARS

from wunderlist import icons
from wunderlist.models.list import List
from wunderlist.models.preferences import Preferences
from wunderlist.models.task import Task
from wunderlist.util import workflow

_hashtag_prompt_pattern = r'#\S*$'

def filter(args):
    query = ' '.join(args[1:])
    wf = workflow()
    prefs = Preferences.current_prefs()
    matching_hashtags = []

    if not query:
        wf.add_item('Begin typing to search tasks', '', icon=icons.SEARCH)

    hashtag_match = re.search(_hashtag_prompt_pattern, query)
    if hashtag_match:
        from wunderlist.models.hashtag import Hashtag

        hashtag_prompt = hashtag_match.group()
        hashtags = Hashtag.select().where(Hashtag.id.contains(hashtag_prompt))

        for hashtag in hashtags:
            # If there is an exact match, do not show hashtags
            if hashtag.id.lower() == hashtag_prompt.lower():
                matching_hashtags = []
                break

            matching_hashtags.append(hashtag)

    # Show hashtag prompt if there is more than one matching hashtag or the
    # hashtag being typed does not exactly match the single matching hashtag
    if len(matching_hashtags) > 0:
        for hashtag in matching_hashtags:
            wf.add_item(hashtag.id[1:], '', autocomplete=u'-search %s %s ' % (query[:hashtag_match.start()], hashtag.id), icon=icons.HASHTAG)

    else:
        conditions = True
        lists = workflow().stored_data('lists')
        matching_lists = lists
        query = ' '.join(args[1:])

        if len(args) > 1:
            components = re.split(r':\s*', query, 1)
            list_query = components[0]
            if list_query:
                matching_lists = workflow().filter(
                    list_query,
                    lists,
                    lambda l: l['title'],
                    # Ignore MATCH_ALLCHARS which is expensive and inaccurate
                    match_on=MATCH_ALL ^ MATCH_ALLCHARS
                )

                # If no matching list search against all tasks
                if matching_lists:
                    query = components[1] if len(components) > 1 else ''

        if len(matching_lists) > 1:
            for l in matching_lists:
                icon = icons.INBOX if l['list_type'] == 'inbox' else icons.LIST
                wf.add_item(l['title'], autocomplete='-search %s: ' % l['title'], icon=icon)
        elif matching_lists:
            conditions = conditions & (Task.list == matching_lists[0]['id'])

        if len(matching_lists) <= 1:
            for arg in query.split(' '):
                if len(arg) > 1:
                    conditions = conditions & Task.title.contains(arg)

            if conditions:
                if not prefs.show_completed_tasks:
                    conditions = Task.completed_at.is_null() & conditions

                tasks = Task.select().where(Task.list.is_null(False) & conditions)

                # Default Wunderlist sort order
                tasks = tasks.join(List).order_by(Task.order.asc(), List.order.asc())

                # Avoid excessive results
                tasks = tasks.limit(50)

                for t in tasks:
                    wf.add_item(u'%s – %s' % (t.list_title, t.title), t.subtitle(), autocomplete='-task %s  ' % t.id, icon=icons.TASK_COMPLETED if t.completed else icons.TASK)


            if prefs.show_completed_tasks:
                wf.add_item('Hide completed tasks', arg='-pref show_completed_tasks --alfred %s' % ' '.join(args), valid=True, icon=icons.HIDDEN)
            else:
                wf.add_item('Show completed tasks', arg='-pref show_completed_tasks --alfred %s' % ' '.join(args), valid=True, icon=icons.VISIBLE)

        wf.add_item('Let\'s discuss this screen', 'Do you need to search completed tasks, tasks by list, date, etc?', arg=' '.join(args + ['discuss']), valid=True, icon=icons.DISCUSS)

        wf.add_item('New search', autocomplete='-search ', icon=icons.CANCEL)
        wf.add_item('Main menu', autocomplete='', icon=icons.BACK)

def commit(args, modifier=None):
    action = args[1]

    if action == 'discuss':
        import webbrowser

        webbrowser.open('https://github.com/idpaterson/alfred-wunderlist-workflow/issues/95')
