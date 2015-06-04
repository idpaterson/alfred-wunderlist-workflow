// Automatically inject Bower components into the app

'use strict';

module.exports = {
	app: {
		src: ['<%= paths.app %>/**/*.html'],
		options: {
			exclude: [
				/ionic.css/
			]
		}
	}
};