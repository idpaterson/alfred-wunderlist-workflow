// Make sure code styles are up to par and there are no obvious mistakes

'use strict';

module.exports = {
	options: {
		// Traverse directories up to the nearest .jshintrc
		jshintrc: true,
		reporter: require('jshint-stylish')
	},
	all: [
		'Gruntfile.js',
		'<%= paths.app %>/**/*.js',
		'<%= paths.grunt_tasks %>/**/*.js',
	]
};