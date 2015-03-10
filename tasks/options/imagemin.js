'use strict';

module.exports = {
	dist: {
		files: [
			// Workflow icon
			{
				expand: true,
				cwd: '<%= paths.app_icons %>',
				dest: '<%= paths.dist_app %>',
				src: 'icon.png'
			},
			// Script filter icons
			{
				expand: true,
				cwd: '<%= paths.app %>',
				dest: '<%= paths.dist_app %>',
				src: [
					'<%= paths.icons_dirname %>/*/**/*.png'
				]
			}
		]
	},
	wwww: {
		files: [{
			expand: true,
			cwd: '<%= paths.www %>',
			dest: '<%= paths.dist_www %>',
			src: [
				'**/*.{gif,jpg,png}'
			]
		}]
	}
};