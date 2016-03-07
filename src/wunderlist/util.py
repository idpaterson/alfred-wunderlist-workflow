from workflow import Workflow
import calendar
from datetime import datetime

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

    return _workflow

def parsedatetime_calendar():
    from parsedatetime import Calendar, Constants

    return Calendar(parsedatetime_constants())

def parsedatetime_constants():
    import locale
    from parsedatetime import Constants

    loc = locale.getlocale(locale.LC_TIME)[0]

    if not loc:
        # In case the LC_* environment variables are misconfigured, catch
        # an exception that may be thrown
        try:
            loc = locale.getdefaultlocale()[0]
        except:
            loc = 'en_US'

    return Constants(loc)

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

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    return local_dt.replace(microsecond=utc_dt.microsecond)
