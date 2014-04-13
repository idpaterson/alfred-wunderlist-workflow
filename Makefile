#
# Wunderlist 2 Alfred Workflow
# Author: Ian Paterson
#
# Usage:
# 	make       Build or update Wunderlist.alfredworkflow distributable
# 	make clean Remove build files and distributable
# 	make docs  Generate documentation in docs/ with HeaderDoc
#

FULL_VERSION := `git describe --abbrev=0`
VERSION := `git describe --abbrev=0 | sed 's/-.*//'`

all: Wunderlist.alfredworkflow

# Prepares the workflow for a release
# Requires a value for the RELEASE_NOTES macro
#   make release RELEASE_NOTES="Foo"
release: update-version-numbers clean Wunderlist.json build/licenses Wunderlist.alfredworkflow

# The installable workflow
Wunderlist.alfredworkflow: build build/info.plist build/wunderlist.scpt build/filters.php build/icons build/localization build/update.json
	cd build/ && zip -r ../Wunderlist.alfredworkflow *

# An installable workflow that uses symlinks to continually
# update from the build directory of this project.
Wunderlist-symlinked.alfredworkflow: Wunderlist.alfredworkflow
	mkdir -p build-symlinks
	ln -s `pwd`/build/* build-symlinks/
	cd build-symlinks/ && zip --symlinks -r ../Wunderlist-symlinked.alfredworkflow *
	rm -rf build-symlinks

build:
	mkdir build/

build/info.plist: source/info.plist
	cp source/info.plist build/

build/wunderlist.applescript: build source/*.applescript source/*/*.applescript source/*/*/*.applescript
	cp source/wunderlist.applescript build/wunderlist.applescript
	# Replace all #includes with the file contents
	perl -i -e '$$/=undef;$$_=<>;s@#include "(.*?)"@open F, "source/$$1.applescript";<F>@ge;print' build/wunderlist.applescript
	# Remove all comments that can be removed safely, because they are
	# not compiled out.
	perl -i -e '$$/=undef;$$_=<>;s/^\s*(#.*|--.*|\(\*![\s\S]*?\*\))\s?//gm;print' build/wunderlist.applescript 

build/wunderlist.scpt: build build/wunderlist.applescript build/bin/q_notifier.helper build/bin/cliclick lib/qWorkflow/compiled\ source/q_workflow.scpt
	osacompile -x -o build/wunderlist.scpt build/wunderlist.applescript
	rm build/wunderlist.applescript

build/filters.php: build source/filters.php build/workflows.php build/CFPropertyList
	cp source/filters.php build/

build/workflows.php: lib/Workflows/workflows.php
	cp lib/Workflows/workflows.php build/

build/CFPropertyList: lib/CFPropertyList/classes/CFPropertyList
	cp -r lib/CFPropertyList/classes/CFPropertyList build/

build/bin:
	mkdir -p build/bin

build/bin/q_notifier.helper: build build/bin
	cp -r lib/qWorkflow/compiled\ source/bin/q_notifier.helper build/bin/

build/bin/cliclick: build build/bin lib/cliclick
	cd lib/cliclick && make 
	cp lib/cliclick/cliclick build/bin/cliclick

build/licenses: build/licenses/alfred-wunderlist-workflow build/licenses/cliclick build/licenses/CFPropertyList

build/licenses/alfred-wunderlist-workflow: LICENSE
	mkdir -p build/licenses/alfred-wunderlist-workflow
	cp LICENSE build/licenses/alfred-wunderlist-workflow/

build/licenses/cliclick: lib/cliclick/LICENSE
	mkdir -p build/licenses/cliclick
	cp lib/cliclick/LICENSE build/licenses/cliclick/

build/licenses/CFPropertyList: lib/CFPropertyList/LICENSE
	mkdir -p build/licenses/CFPropertyList
	cp lib/CFPropertyList/LICENSE build/licenses/CFPropertyList/

build/localization: build source/localization
	cp -r source/localization/* build/
	plutil -convert binary1 build/*.lproj/*.strings

build/icons: build
	cp source/icons/icon.png build/
	cp source/icons/wunderlist_inbox.png build/D14D2445-537F-4FA7-B0E0-1FCAEE7CD292.png
	cp source/icons/wunderlist_list.png build/954FB09A-0A22-450E-A5D6-0F58EC3760A0.png
	cp -r source/icons/lists build/

# Alleyoop current version metadata
build/update.json: build
	cp source/alleyoop/update.json.mustache build/update.json
	sed -i "" "s/{{ *version *}}/${VERSION}/" build/update.json

# Alleyoop newest available version metadata
Wunderlist.json: require-release-notes
	cp source/alleyoop/Wunderlist.json.mustache Wunderlist.json
	sed -i "" "s/{{ *version *}}/${VERSION}/" Wunderlist.json

	# Escape release notes to avoid breaking the regex syntax
	sed -i "" "s/{{ *release_notes *}}/`echo ${RELEASE_NOTES} | sed -e 's/[\/&]/\\\\&/g'`/" Wunderlist.json

# Installs the workflow from build/ in Wunderlist using symlinks.
# Subsequent make commands will update the workflow in Alfred.
develop: Wunderlist-symlinked.alfredworkflow
	open Wunderlist-symlinked.alfredworkflow

# Installs the workflow from build/ in Wunderlist.
# All files are copied, subsequent make commands will not update the 
# workflow in Alfred.
install: Wunderlist.alfredworkflow
	open Wunderlist.alfredworkflow


# If the make command did not specify RELEASE_NOTES="Foo" the release
# cannot be built
require-release-notes:
    ifndef RELEASE_NOTES
		$(error Must define RELEASE_NOTES macro to release)
    endif

update-version-numbers:
	perl -p -i -e "s/(\@version\s*)\S.*/\$${1}${FULL_VERSION}/" source/*.applescript source/*/*.applescript source/*/*/*.applescript source/*.php

deps:
	brew install gettext
	brew link gettext

headerdoc/headerDoc2HTML.pl:
	wget http://opensource.apple.com/tarballs/headerdoc/headerdoc-8.9.14.tar.gz
	tar xvf headerdoc-8.9.14.tar.gz
	rm headerdoc-8.9.14.tar.gz
	mv headerdoc-8.9.14 headerdoc
	patch -p1 < source/headerdoc-patch.diff
	#cd headerdoc && wget http://www.darwin-development.org/headerdoc_patches/Xcode_5/headerdoc-8.9.24-8.9.25.diff && patch -p1 < headerdoc-8.9.24-8.9.25.diff
	#cd headerdoc && wget http://www.darwin-development.org/headerdoc_patches/Xcode_5/headerdoc-8.9.25-8.9.26.diff && patch -p1 < headerdoc-8.9.25-8.9.26.diff
	cd headerdoc && make all_internal -i
	# Install a patched version of HeaderDoc that works with AppleScript
	#cd headerdoc && sudo make realinstall

# Removes intermediary build files
clean:
	rm -rf build/
	rm -rf Wunderlist.alfredworkflow Wunderlist-symlinked.alfredworkflow Wunderlist.json

# Generates documentation in gh-pages branch submodule at docs/
docs: headerdoc/headerDoc2HTML.pl source/*.applescript source/*/*.applescript source/*/*/*.applescript source/*.php
	# Delete old docs without removing the .git directory
	find docs/* -type d -not -name '.git' | xargs rm -rf
	headerdoc/headerDoc2HTML.pl -o docs source/*.applescript source/*/*.applescript source/*/*/*.applescript source/*.php
	headerdoc/gatherHeaderDoc.pl docs

.PHONY: all clean docs build/localization build/icons build/update.json Wunderlist.json require-release-notes update-version-numbers
