#
# Wunderlist 2 Alfred Workflow
# Author: Ian Paterson
#
# Usage:
# 	make       Build or update Wunderlist.alfredworkflow distributable
# 	make clean Remove build files and distributable
# 	make docs  Generate documentation in docs/ with HeaderDoc
#

VERSION := `git describe --abbrev=0 | sed 's/-.*//'`

all: Wunderlist.alfredworkflow

# Prepares the workflow for a release
# Requires a value for the RELEASE_NOTES macro
#   make release RELEASE_NOTES="Foo"
release: Wunderlist.json Wunderlist.alfredworkflow

# The installable workflow
Wunderlist.alfredworkflow: build build/info.plist build/wunderlist.scpt build/q_workflow.scpt build/icons build/localization build/update.json
	cd build/ && zip -r ../Wunderlist.alfredworkflow *

build:
	mkdir build/

build/info.plist: source/info.plist
	cp source/info.plist build/

build/wunderlist.scpt: source/wunderlist.applescript
	osacompile -x -o build/wunderlist.scpt source/wunderlist.applescript

build/q_workflow.scpt: build/bin lib/qWorkflow/compiled\ source/q_workflow.scpt
	osacompile -x -o build/q_workflow.scpt lib/qWorkflow/compiled\ source/q_workflow.scpt

build/bin: lib/qWorkflow/compiled\ source/bin
	cp -r lib/qWorkflow/compiled\ source/bin build/

build/localization: source/localization
	cp -r source/localization/* build/

build/icons:
	cp source/icons/icon.png build/
	cp source/icons/wunderlist_inbox.png build/D14D2445-537F-4FA7-B0E0-1FCAEE7CD292.png
	cp source/icons/wunderlist_list.png build/954FB09A-0A22-450E-A5D6-0F58EC3760A0.png
	cp -r source/icons/lists build/

# Alleyoop current version metadata
build/update.json:
	cp source/update.json.mustache build/update.json
	sed -i "" "s/{{ *version *}}/${VERSION}/" build/update.json

# Alleyoop newest available version metadata
Wunderlist.json: require-release-notes
	cp source/Wunderlist.json.mustache Wunderlist.json
	sed -i "" "s/{{ *version *}}/${VERSION}/" Wunderlist.json
	sed -i "" "s/{{ *release_notes *}}/${RELEASE_NOTES}/" Wunderlist.json

# If the make command did not specify RELEASE_NOTES="Foo" the release
# cannot be built
require-release-notes:
    ifndef RELEASE_NOTES
		$(error Must define RELEASE_NOTES macro to release)
    endif

# Removes intermediary build files
clean:
	rm -rf build/
	rm -rf Wunderlist.alfredworkflow Wunderlist.json

# Generates documentation in gh-pages branch submodule at docs/
docs: source/wunderlist.applescript
	headerdoc2html -o docs source/wunderlist.applescript
	mv docs/wunderlist_applescript/* docs/
	rm -rf docs/wunderlist_applescript
	gatherheaderdoc docs
	rm docs/masterTOC.html

.PHONY: all clean build/localization build/icons build/update.json Wunderlist.json require-release-notes