Wunderlist Workflow for Alfred
==========================

Create tasks and lists in [Wunderlist 2 for OS X](http://appstore.com/mac/Wunderlist) from [Alfred 2](http://www.alfredapp.com/) (requires Powerpack license).

![Adding a task to Wunderlist](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/gh-pages/images/screenshots/add_task_to_list.jpg)

Setup
-----

### [Download](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/master/Wunderlist.alfredworkflow)

Download the latest stable version of this workflow [here](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/master/Wunderlist.alfredworkflow). After downloading, simply double-click to install the workflow in Alfred. 

The workflow can also be built from source. After cloning the repository, just call `make` from the project directory to build `Wunderlist.alfredworkflow` locally, then double-click to install. [The documentation](http://idpaterson.github.io/alfred-wunderlist-workflow/) and [test cases](https://github.com/idpaterson/alfred-wunderlist-workflow/blob/master/TESTING.md) should be helpful for anyone wishing to work on this project; please submit a pull request if you add anything that others might appreciate!

### Enable *Access for Assistive Devices*
In order to interact with Wunderlist, your computer must allow scripts like this workflow to communicate with other apps.

In OS X Mavericks:

1. Install and use any of the commands in this workflow
2. Open *System Preferences*
3. *Security & Privacy*
4. *Privacy*
5. *Accessibility*
6. Click the lock in the lower left corner to make changes
7. Check the checkbox beside *Alfred.app* 

In OS X Mountain Lion:

1. Open *System Preferences*
2. *Accessibility*
3. In the lower left, check the box next to *Enable access for assistive devices*

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

The current implementation relies heavily on keyboard navigation and shortcuts in Wunderlist 2 because it does [not yet](http://www.alfredforum.com/topic/1302-workflow-for-wunderlist-2/?p=8074) provide bindings for AppleScript. Improvements in this direction could make it possible to create and manage tasks with more fine-grained control over attributes such as due dates and Pro features. Please submit feature requests so that the workflow can be updated once Wunderlist 2 becomes more accessible via a public API or AppleScript bindings.

Currently it does not seem possible to reliably control the following features. A click emulator such as [cliclick](http://www.bluem.net/en/mac/cliclick/) may be necessary in order to interact with some of the buttons that are not keyboard accessible:

* Starred tasks (workaround: add tasks to the Starred list)
* Due dates
* Reminders
* Subtasks
* Notes
* Completing tasks
* Moving tasks
* Sorting lists
* Pro features

The following may be possible but would require significant effort.

* Displaying tasks in Alfred (see discussion in [getTaskInfoForFocusedList()](http://idpaterson.github.io/alfred-wunderlist-workflow/index.html#//apple_ref/applescript/func/getTaskInfoForFocusedList))
* Deleting specific tasks
* Editing specific tasks
* Displaying the number of tasks in a list (see discussion in [getListInfo()](http://idpaterson.github.io/alfred-wunderlist-workflow/index.html#//apple_ref/applescript/func/getListInfo))

Acknowledgements
----------------

This workflow relies on [qWorkflow](https://github.com/qlassiqa/qWorkflow) by [Ursan Razvan](https://github.com/qlassiqa) to communicate with Alfred. The qWorkflow library is bundled with the workflow in a compiled format and also included with the workflow source as a submodule.

Alternatives
------------

* [Wunderlist extension for Alfred 1](https://github.com/jdfwarrior/Wunderlist) by [David Ferguson](https://github.com/jdfwarrior)
* [Wunderlist 2 for Alfred](https://github.com/sebietter/Wunderlist-2-for-Alfred) by [sebietter](https://github.com/sebietter)