// Copies remaining files to places other tasks can use

'use strict';

module.exports = {
	options: {
		mode: 'zip',
		pretty: true
	},
	workflow: {
		options: {
			archive: '<%= paths.dist_workflow %>',
			level: 9
		},
		files: [{
			expand: true,
			cwd: '<%= paths.dist_app %>',
			src: [
				'**/*',
				'!**/*.{pyc,pyo}'
			]
		}]
	}
};