from workflow import Workflow

_workflow = None

def workflow():
	global _workflow

	if _workflow is None:
		_workflow = Workflow()

	return _workflow