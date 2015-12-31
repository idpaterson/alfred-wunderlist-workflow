
'use strict';

module.exports = function(grunt) {
	grunt.registerTask('build', [
		'copy:dist',
		'newer:imagemin:dist',
		'newer:symlink:workflow',
		'replace',
		'compress:workflow',
		'shell:symlinkWorkflow'
	]);
};