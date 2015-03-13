// Replace text in files

'use strict';

module.exports = {
	dist: {
		src: '<%= paths.dist %>/**/*.{py,html,js,css}',
		overwrite: true,
		replacements: [
			{
				from: '__VERSION__',
				to: '<%= pkg.version %>'
			},
			{
				from: '__BUILD_DATE__',
				to: '<%= grunt.template.today("mediumDate") %>'
			}
		]
	}
};