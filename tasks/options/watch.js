// Watches for changes to files

'use strict';

module.exports = {
	app: {
		files: ['<%= paths.app %>/**/*'],
		tasks: ['build']
	},
	grunt: {
		files: [
			'Gruntfile.js',
			'<%= paths.grunt_tasks %>/**/*'
		],
		options: {
			reload: true
		}
	}
};