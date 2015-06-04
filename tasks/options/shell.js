// Runs shell commands

'use strict';

module.exports = {
	symlinkWorkflow: {
		options: {
			execOptions: {
				cwd: '<%= paths.tmp_workflow_symlinked %>'
			}
		},
		command: 'zip --symlinks -r ../../<%= paths.dist_workflow_symlinked %> *'
	},

	pyTest: {
		options: {
			execOptions: {
				cwd: '<%= paths.dist_app %>'
			}
		},
		command: 'PYTHONPATH=. py.test ../../<%= paths.tests %> --cov-report term-missing --cov wunderlist'
	}
};