from wunderlist.models import base, root, list, task, user

def _setup():
	base.BaseModel._meta.database.create_tables([
		root.Root,
		list.List,
		task.Task,
		user.User
	], safe=True)

def sync():
	_setup()

	root.Root.sync()