import json

import requests

from wunderlist import config
from wunderlist.auth import oauth_token

_oauth_token = None

def _request_headers():
    global _oauth_token

    if not _oauth_token:
        _oauth_token = oauth_token()

    if _oauth_token:
        return {
            'x-access-token': _oauth_token,
            'x-client-id': config.WL_CLIENT_ID,
            'content-type': 'application/json'
        }
    return None

def _report_errors(fn):
    def report_errors(*args, **kwargs):
        response = fn(*args, **kwargs)
        if response.status_code > 500:
            response.raise_for_status()
        return response
    return report_errors

def get(path, params=None):
    headers = _request_headers()
    return requests.get(
        config.WL_API_BASE_URL + '/' + path,
        headers=headers,
        params=params
    )

@_report_errors
def post(path, data=None):
    headers = _request_headers()
    return requests.post(
        config.WL_API_BASE_URL + '/' + path,
        headers=headers,
        data=json.dumps(data)
    )

@_report_errors
def put(path, data=None):
    headers = _request_headers()
    return requests.put(
        config.WL_API_BASE_URL + '/' + path,
        headers=headers,
        data=json.dumps(data)
    )

@_report_errors
def patch(path, data=None):
    headers = _request_headers()
    return requests.patch(
        config.WL_API_BASE_URL + '/' + path,
        headers=headers,
        data=json.dumps(data)
    )

@_report_errors
def delete(path, data=None):
    headers = _request_headers()
    return requests.delete(
        config.WL_API_BASE_URL + '/' + path,
        headers=headers,
        params=data
    )
