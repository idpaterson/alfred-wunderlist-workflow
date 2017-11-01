from datetime import date, datetime, timedelta
import logging

from workflow import Workflow

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

_workflow = None
_update_settings = None


def workflow():
    global _workflow, _update_settings

    if _workflow is None:
        version = '__VERSION__'

        _workflow = Workflow(
            capture_args=False,
            update_settings={
                'github_slug': 'idpaterson/alfred-wunderlist-workflow',
                'version': version,
                # Check for updates daily
                # TODO: check less frequently as the workflow becomes more
                # stable
                'frequency': 1,
                # Always download pre-release updates if a prerelease is
                # currently installed
                'prerelease': '-' in version
            }
        )

        # Avoid default logger output configuration
        _workflow.logger = logging.getLogger('workflow')

    return _workflow


def parsedatetime_calendar():
    from parsedatetime import Calendar, Constants

    return Calendar(parsedatetime_constants())


def parsedatetime_constants():
    from parsedatetime import Constants
    from wunderlist.models.preferences import Preferences

    loc = Preferences.current_prefs().date_locale or user_locale()

    return Constants(loc)


def user_locale():
    import locale

    loc = locale.getlocale(locale.LC_TIME)[0]

    if not loc:
        # In case the LC_* environment variables are misconfigured, catch
        # an exception that may be thrown
        try:
            loc = locale.getdefaultlocale()[0]
        except IndexError:
            loc = 'en_US'

    return loc

def format_time(time, format):
    c = parsedatetime_constants()

    expr = c.locale.timeFormats[format]
    expr = (expr
            .replace('HH', '%H')
            .replace('h', '%I')
            .replace('mm', '%M')
            .replace('ss', '%S')
            .replace('a', '%p')
            .replace('z', '%Z')
            .replace('v', '%z'))

    return time.strftime(expr).lstrip('0')


def short_relative_formatted_date(dt):
    d = dt.date() if isinstance(dt, datetime) else dt
    today = date.today()
    # Mar 3, 2016
    date_format = '%b %d, %Y'

    if d == today:
        return 'today'
    if d == today + timedelta(days=1):
        return 'tomorrow'
    elif d == today - timedelta(days=1):
        return 'yesterday'
    elif d.year == today.year:
        # Wed, Mar 3
        date_format = '%a, %b %d'

    return dt.strftime(date_format)

def relaunch_alfred(command='wl'):
    import subprocess

    alfred_major_version = workflow().alfred_version.tuple[0]

    subprocess.call([
        '/usr/bin/env', 'osascript', '-l', 'JavaScript',
        'bin/launch_alfred.scpt', command, str(alfred_major_version)
    ])

def utc_to_local(utc_dt):
    import calendar
    
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    return local_dt.replace(microsecond=utc_dt.microsecond)
