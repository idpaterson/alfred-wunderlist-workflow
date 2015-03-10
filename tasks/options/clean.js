// Removes generated files

'use strict';

module.exports = {
	dist: [
		'<%= paths.dist %>',
		'<%= paths.dist_workflow %>',
		'<%= paths.dist_workflow_symlinked %>',
	],
	tmp: [
		'<%= paths.tmp %>'
	]
};