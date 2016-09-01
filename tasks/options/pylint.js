// Validates python source

'use strict';

module.exports = {
	options: {
		rcfile: '.pylintrc'
	},
	app: {
		src: '<%= paths.app_module %>'
	}
};