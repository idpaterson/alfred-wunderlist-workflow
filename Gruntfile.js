/*
 * Author: Ian Paterson
 * Grunt Commands
 */

'use strict';

var grunt = require('grunt');

// Creates an object with keys representing each file in the path assigned to
// the exported value of the file's module.
function loadConfig(path) {
	var object = {};
	var key;

	grunt.file.expand({ cwd: path + '/' }, '*.js').forEach(function(filename) {
		key = filename.replace(/\.js$/,'');
		object[key] = require(path + '/' + filename);
	});

	return object;
}

module.exports = function(grunt) {
	// Load grunt tasks automatically
	// No need for grunt.loadNpmTasks('some-package');
	require('load-grunt-tasks')(grunt);

	// Time how long tasks take. Can help when optimizing build times
	require('time-grunt')(grunt);

	// Load custom tasks
	grunt.loadTasks('./tasks');

	var config = loadConfig('./tasks/options');

	grunt.initConfig(config);

	console.log(grunt.config());
};
