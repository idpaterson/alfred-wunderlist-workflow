import json
import requests
from wunderlist.auth import oauth_token
from wunderlist import config

def _request_headers():
	token = oauth_token()

	if token:
		return {
			'x-access-token': token,
			'x-client-id': config.WL_CLIENT_ID,
			'content-type': 'application/json'
		}
	return None

def get(path, params=None):
	headers = _request_headers()
	return requests.get(
		config.WL_API_BASE_URL + '/' + path,
		headers=headers,
		params=params
	)

def post(path, data=None):
	headers = _request_headers()
	return requests.post(
		config.WL_API_BASE_URL + '/' + path,
		headers=headers,
		data=json.dumps(data)
	)

def put(path, data=None):
	headers = _request_headers()
	return requests.put(
		config.WL_API_BASE_URL + '/' + path,
		headers=headers,
		data=json.dumps(data)
	)

def patch(path, data=None):
	headers = _request_headers()
	return requests.patch(
		config.WL_API_BASE_URL + '/' + path,
		headers=headers,
		data=json.dumps(data)
	)

def delete(path, data=None):
	headers = _request_headers()
	return requests.delete(
		config.WL_API_BASE_URL + '/' + path,
		headers=headers,
		data=json.dumps(data)
	)