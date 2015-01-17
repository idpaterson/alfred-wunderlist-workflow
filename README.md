Wunderlist Workflow for Alfred
==========================

Create tasks and lists in [Wunderlist 3 for OS X](http://appstore.com/mac/Wunderlist) from [Alfred 2](http://www.alfredapp.com/) (requires Powerpack license).

:exclamation: **OS X Yosemite has broken critical features that this workflow relied on.** The workflow does not function in Yosemite and cannot be fixed without changes to Yosemite or Wunderlist's UI. Please subscribe to [this discussion](https://github.com/idpaterson/alfred-wunderlist-workflow/issues/44) for updates, to share suggestions, or to participate in testing the next iteration of this workflow.

![Adding a task to Wunderlist](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/gh-pages/images/screenshots/add_task_to_list.jpg)

Setup
-----

### [Download](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/master/Wunderlist.alfredworkflow)

Download the latest stable version of this workflow [here](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/master/Wunderlist.alfredworkflow). After downloading, simply double-click to install the workflow in Alfred. 

The workflow can also be built from source. After cloning the repository, just call `make install` from the project directory to build and install `Wunderlist.alfredworkflow`. 

### Enable *Access for Assistive Devices*
In order to interact with Wunderlist, your computer must allow scripts like this workflow to communicate with other apps. If accessibility is not enabled, the workflow will pop up a notification and take you to a settings page. Simply enable the checkbox beside `Alfred 2.app`. [More details here.](http://support.apple.com/kb/HT6026)

Features
--------

### Add a new task to any list

To add a task to a list other than the inbox, use the Alfred shortcut `wl`, followed by the text of the task. Select the appropriate list from those shown by using the arrow keys to highlight the desired list, then press Return to add the task. If you do not select a list, the task will be added in whichever list is currently visible in Wunderlist.

	wl Recycle used ink cartridges

You can also type the name of a list followed by a colon to add the task in a specific list. Simply begin typing the list name then press `tab` or `return` to autocomplete the name of the list. Autocompletion allows efficient task entry using just a few keystrokes.

	wl off                                  -- Alfred shows lists containing "off"
	wl Office:                              -- Press tab to autocomplete the list name
	wl Office:Recycle used ink cartridges   -- Type the task then press return

Autocompletion also allows adding tasks based on just a portion of the list name. Simply type a few letters in the list name followed by a colon and the text of the task.

	wl off:Recycle used ink cartridges

### Add a new task to the inbox

To add a task directly to the inbox, use the Alfred shortcut `wlin`, followed by the text of the task. The new task will be added in your inbox, allowing you to later file it into the appropriate folder. This is often the easiest way to add tasks quickly and avoid getting distracted by categorization.

	wlin Recycle used ink cartridges

After entering the task, you will be returned to whichever application you were using prior to adding the task. Wunderlist will also be returned to whichever list you were viewing prior to the inbox. 

Used without any arguments, `wlin` simply opens Wunderlist to the inbox. 

**Note** This command may eventually be removed in favor of `wl in:Recycle used ink cartridges`, which could work better for different localizations of Wunderlist. For example, Spanish language users will add tasks to their *Bandeja de entrada*, so `wlin` does not make as much sense as `wl ba:` or `wl en:`.

### Add a new list 

To add a new list, use the Alfred shortcut `wllist`, followed by the name of the list. The new list will be added and Wunderlist will remain active, allowing you to add new tasks to the list.

	wllist Grocery List

Limitations
-----------

The current implementation relies heavily on keyboard navigation and mouse clicks in Wunderlist 3, which does [not yet](http://www.alfredforum.com/topic/1302-workflow-for-wunderlist-2/?p=8074) provide bindings for AppleScript. Improvements in this direction could make it possible to create and manage tasks with more fine-grained control over attributes such as due dates and Pro features. Please submit feature requests so that the workflow can be updated once Wunderlist 3 becomes more accessible via a public API or AppleScript bindings!

Testing
-------

Simply run `./run_tests.sh` to be guided through all of the tests in a semi-automated process that puts you in control of setting up the correct preconditions and passing or failing each test. [The manual test plan](https://github.com/idpaterson/alfred-wunderlist-workflow/blob/master/TESTING.md) is available for those wishing to follow the steps manually.

Contributing
------------

So you want to help make this workflow better? That's great! Please see [the documentation](http://idpaterson.github.io/alfred-wunderlist-workflow/) for an introduction to the structure of this workflow. After cloning the repository, run `make develop` to build the workflow and install a copy in Alfred containing symlinks to your repository. After making a change, simply run `make` to rebuild the workflow then use Alfred to test. Using this process, the workflow is kept up-to-date while you work.

Always run through the semi-automated tests to ensure that your change does not cause issues elsewhere. When possible, add corresponding tests for your contributions. Be sure to add human-readable steps to `TESTING.md` as well as corresponding `tests/x.x.x - Test name.applescript` files. You can run individual tests with `./run_tests.sh 1.2.3` or specific test suites such as `./run_tests.sh 1` or `./run_tests.sh 1.2` to run all 1.x.x or 1.2.x, respectively.

Acknowledgements
----------------

This workflow relies on [qWorkflow](https://github.com/qlassiqa/qWorkflow) by [Ursan Razvan](https://github.com/qlassiqa) to communicate with Alfred. The qWorkflow library is bundled with the workflow in a compiled format and also included with the workflow source as a submodule.

The [cliclick](www.bluem.net/en/mac/cliclick/) utility by [Carsten Blüm](https://github.com/BlueM) allows the workflow to perform mouse clicks, unlocking much functionality that is not easily keyboard-accessible in Wunderlist. The cliclick utility is bundled with the workflow in a compiled format and also included with the workflow source as a submodule.

Alternatives
------------

* [Wunderlist extension for Alfred 1](https://github.com/jdfwarrior/Wunderlist) by [David Ferguson](https://github.com/jdfwarrior)
* [Wunderlist 2 for Alfred](https://github.com/sebietter/Wunderlist-2-for-Alfred) by [sebietter](https://github.com/sebietter)
