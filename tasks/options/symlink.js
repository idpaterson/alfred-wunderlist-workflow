// Copies remaining files to places other tasks can use

'use strict';

module.exports = {
	options: {
		overwrite: true
	},
	workflow: {
		files: [{
			expand: true,
			cwd: process.cwd() + '/<%= paths.dist_app %>',
			dest: '<%= paths.tmp_workflow_symlinked %>/',
			src: '*'
		}]
	}
};