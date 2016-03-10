import wunderlist.api.base as api


def settings():
    req = api.get('settings')
    settings = req.json()

    return settings
