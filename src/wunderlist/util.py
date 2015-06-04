from workflow import Workflow

_workflow = None

def workflow():
	global _workflow

	if _workflow is None:
		_workflow = Workflow(
			capture_args=False,
			update_settings={
				'github_slug': 'idpaterson/alfred-wunderlist-workflow',
				'version': '__VERSION__',
				# Check for updates daily
				# TODO: check less frequently as the workflow becomes more
				# stable
				'frequency': 1
			}
		)

	return _workflow