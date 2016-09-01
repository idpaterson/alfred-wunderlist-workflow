'use strict';

module.exports = {
	node_modules: 'node_modules',
	lib: '<%= paths.lib_dirname %>',

	// Directory names
	// for consistent directories across app, .tmp, www, and dist
	app_dirname: 'src',
	bin_dirname: 'bin',
	lib_dirname: 'lib',
	www_dirname: 'www',
	dist_dirname: 'dist',
	icons_dirname: 'icons',
	images_dirname: 'images',
	scripts_dirname: 'scripts',
	styles_dirname: 'styles',

	// Source code
	app: '<%= paths.app_dirname %>',
	app_bin: '<%= paths.app %>/<%= paths.bin_dirname %>',
	app_lib: '<%= paths.app %>/<%= paths.lib_dirname %>',
	app_module: '<%= paths.app %>/wunderlist',
	app_icons: '<%= paths.app %>/<%= paths.icons_dirname %>',

	// Documentation and marketing
	www: '<%= paths.www_dirname %>',
	images: '<%= paths.www %>/<%= paths.images_dirname %>',
	scripts: '<%= paths.www %>/<%= paths.scripts_dirname %>',
	styles: '<%= paths.www %>/<%= paths.styles_dirname %>',

	tests: 'tests',

	// Built distribution
	dist: '<%= paths.dist_dirname %>',

	dist_app: '<%= paths.dist %>/workflow',
	dist_bin: '<%= paths.dist_app %>/<%= paths.bin_dirname %>',
	dist_lib: '<%= paths.dist_app %>',
	dist_icons: '<%= paths.dist_app %>/<%= paths.icons_dirname %>',

	dist_www: '<%= paths.dist %>/<%= paths.www_dirname %>',
	dist_fonts: '<%= paths.dist_www %>/<%= paths.fonts_dirname %>',
	dist_styles: '<%= paths.dist_www %>/<%= paths.styles_dirname %>',
	dist_scripts: '<%= paths.dist_www %>/<%= paths.scripts_dirname %>',
	dist_images: '<%= paths.dist_www %>/<%= paths.images_dirname %>',

	// Final binaries, make them easy to find in the repo root
	dist_workflow: 'Wunderlist.alfredworkflow',
	dist_workflow_symlinked: 'Wunderlist-symlinked.alfredworkflow',

	// Temporary paths
	tmp: '.tmp',
	tmp_lib: '<%= paths.tmp %>/<%= paths.lib_dirname %>',
	tmp_workflow_symlinked: '<%= paths.tmp %>/workflow-symlinked',

	// Grunt
	grunt_tasks: 'tasks',
	grunt_task_options: '<%= paths.grunt_tasks %>/options'

};