'use strict';

var grunt = require('grunt');

module.exports = grunt.util._.extend({}, grunt.file.readJSON('.bowerrc'), grunt.file.readJSON('bower.json'));