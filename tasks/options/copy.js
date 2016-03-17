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
				cwd: '<%= paths.lib %>/dateutil',
				dest: '<%= paths.dist_lib %>',
				src: [
					'dateutil/**/*.py',
					'!dateutil/tests/**/*'
				]
			},
			{
				expand: true,
				cwd: '<%= paths.lib %>/futures',
				dest: '<%= paths.dist_lib %>',
				src: [
					'concurrent/**/*'
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
					'workflow/**/*.{py,tgz}',
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
			{
				expand: true,
				cwd: '<%= paths.lib %>/six',
				dest: '<%= paths.dist_lib %>',
				src: [
					'six.py'
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