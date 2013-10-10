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
release: update-version-numbers clean Wunderlist.json Wunderlist.alfredworkflow

# The installable workflow
Wunderlist.alfredworkflow: build build/info.plist build/wunderlist.scpt build/filters.php build/icons build/localization build/update.json
	cd build/ && zip -r ../Wunderlist.alfredworkflow *

build:
	mkdir build/

build/info.plist: source/info.plist
	cp source/info.plist build/

build/wunderlist.applescript: build source/*.applescript source/*/*.applescript
	cp source/wunderlist.applescript build/wunderlist.applescript
	# Replace all #includes with the file contents
	perl -i -e '$$/=undef;$$_=<>;s@#include "(.*?)"@open F, "source/$$1.applescript";<F>@ge;print' build/wunderlist.applescript
	# Remove all comments that can be removed safely, because they are
	# not compiled out.
	perl -i -e '$$/=undef;$$_=<>;s/^\s*(#.*|--.*|\(\*![\s\S]*?\*\))\s?//gm;print' build/wunderlist.applescript 

build/wunderlist.scpt: build build/wunderlist.applescript build/bin/q_notifier.helper lib/qWorkflow/compiled\ source/q_workflow.scpt
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

build/localization: build source/localization
	cp -r source/localization/* build/

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

# If the make command did not specify RELEASE_NOTES="Foo" the release
# cannot be built
require-release-notes:
    ifndef RELEASE_NOTES
		$(error Must define RELEASE_NOTES macro to release)
    endif

update-version-numbers:
	perl -p -i -e "s/(\@version\s*)\S.*/\$${1}${FULL_VERSION}/" source/*.applescript source/*/*.applescript source/*.php

deps:
	brew install gettext
	brew link gettext

# Removes intermediary build files
clean:
	rm -rf build/
	rm -rf Wunderlist.alfredworkflow Wunderlist.json

# Generates documentation in gh-pages branch submodule at docs/
docs: source/*.applescript source/*/*.applescript source/*.php
	# Delete old docs without removing the .git directory
	find docs/* -type d -not -name '.git' | xargs rm -rf
	rm -rf docs/*.html
	headerdoc2html -o docs source/*.applescript source/*/*.applescript source/*.php
	gatherheaderdoc docs

.PHONY: all clean build/localization build/icons build/update.json Wunderlist.json require-release-notes update-version-numbers
