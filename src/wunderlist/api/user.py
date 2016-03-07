import wunderlist.api.base as api

def user():
    req = api.get('user')
    user = req.json()

    return user
