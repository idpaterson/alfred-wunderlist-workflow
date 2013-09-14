#
# Wunderlist 2 Alfred Workflow
# Author: Ian Paterson
#
# Usage:
# 	make       Build or update Wunderlist.alfredworkflow distributable
# 	make clean Remove build files and distributable
# 	make docs  Generate documentation in docs/ with HeaderDoc
#

all: Wunderlist.alfredworkflow

Wunderlist.alfredworkflow: build build/info.plist build/wunderlist.scpt build/q_workflow.scpt build/icons build/localization
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

clean:
	rm -rf build/
	rm -rf Wunderlist.alfredworkflow

docs: source/wunderlist.applescript
	headerdoc2html -o docs source/wunderlist.applescript
	mv docs/wunderlist_applescript/* docs/
	rm -rf docs/wunderlist_applescript
	gatherheaderdoc docs
	rm docs/masterTOC.html

.PHONY: all clean build/localization build/icons