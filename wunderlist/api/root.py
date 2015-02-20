import wunderlist.api.base as api

def root():
	req = api.get('root')
	info = req.json()

	return info