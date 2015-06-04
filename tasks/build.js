
'use strict';

module.exports = function(grunt) {
	grunt.registerTask('build', [
		'newer:copy:dist',
		'newer:imagemin:dist',
		'newer:symlink:workflow',
		'replace',
		'compress:workflow',
		'shell:symlinkWorkflow'
	]);
};