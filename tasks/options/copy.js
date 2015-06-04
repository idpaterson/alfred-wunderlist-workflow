// Copies remaining files to places other tasks can use

'use strict';

module.exports = {
	dist: {
		files: [
			{
				expand: true,
				cwd: '<%= paths.app %>',
				dest: '<%= paths.dist_app %>',
				src: [
					'**/*.{py,scpt,plist}'
				]
			},
			{
				expand: true,
				cwd: '<%= paths.lib %>/peewee',
				dest: '<%= paths.dist_lib %>',
				src: [
					'peewee.py'
				]
			},
			{
				expand: true,
				cwd: '<%= paths.lib %>/alfred-workflow/',
				dest: '<%= paths.dist_lib %>',
				src: [
					'workflow/**/*.py',
					'workflow/version'
				]
			},
			{
				expand: true,
				cwd: '<%= paths.lib %>/parsedatetime',
				dest: '<%= paths.dist_lib %>',
				src: [
					'parsedatetime/**/*.py',
					'!parsedatetime/**/tests/**/*'
				]
			},
			{
				expand: true,
				cwd: '<%= paths.lib %>/requests',
				dest: '<%= paths.dist_lib %>',
				src: [
					'requests/**/*.{py,pem}'
				]
			},
			// TODO: remove bundled HTML files once ghpages documentation and
			// landing page are available
			{
				expand: true,
				cwd: '<%= paths.www %>',
				dest: '<%= paths.dist_app %>/www',
				src: [
					'*.html',
				]
			}
		]
	},
};