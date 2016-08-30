Wunderlist Workflow for Alfred
==========================

Create tasks in [Wunderlist](http://wunderlist.com) more effortlessly than ever before with this [Alfred](http://www.alfredapp.com/) workflow (requires Alfred 2 or 3 with a Powerpack license). 

Beginner and advanced approaches to adding a monthly repeating task beginning the following week:

![Simple and advanced usage](https://cloud.githubusercontent.com/assets/507058/7975455/ff5acaea-0a3b-11e5-93f9-74b4b14039dc.gif)

| [Setup](#setup) | [Add Tasks](#add-tasks) | [Due](#due-tasks) | [Upcoming](#upcoming-tasks) | [Search Tasks](#search-tasks) | [Command Shorthand](#command-shorthand) |
| :-------------: | :---------------------: | :---------------: | :-------------------------: | :---------------------------: | :-------------------------------------: |

Setup
-----

### [Download here](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/master/Wunderlist.alfredworkflow)

After downloading, simply double-click to install the workflow in Alfred. Use the `wl` command in Alfred to activate the workflow, or assign a hotkey in Alfred preferences. The workflow will guide you through securely logging in to Wunderlist and will even let you know when an important update is available.

Add tasks
--------

The workflow provides an easy guided experience with tips along the way that will help you become a power user. 

The welcome screen appears when you've typed `wl` (and nothing else). Special commands are in the form `wl-command` with no space; once you type a space after `wl ` you're in task entry mode. Partial commands are matched, so rather than typing `wl-upcoming` to get to the Upcoming tasks list you can type as little as `wlu`.

![Welcome screen](https://cloud.githubusercontent.com/assets/507058/18088099/92f50464-6e86-11e6-9706-d9f4d903dc4d.png)


### Adding tasks with due dates and recurrence

Add your first task! As you type, the workflow will pick out due dates and recurrence intervals in just about any format you could think of. Just write naturally, the due date, recurrence, and task text are updated in Alfred as you type.

![Task with due date and recurrence](https://cloud.githubusercontent.com/assets/507058/11858336/bbcb7c1a-a42e-11e5-85f6-414aa82fcbbb.png)

Use the menus to configure your task until you become a power user capable of typing everything manually. It's so worthwhile to be able to drop tasks into Wunderlist in under a second.

![Due date menu](https://cloud.githubusercontent.com/assets/507058/7895423/d67861e4-065a-11e5-95fa-2bedeb70432b.png)

### Adding tasks to a specific list

To select a list, type it first followed by a colon or use the Change list menu item. No need to type the full list name, as long as you see the correct list in Alfred a few letters is usually sufficient.

![List by substring matching](https://cloud.githubusercontent.com/assets/507058/11858365/e43c56d8-a42e-11e5-9ec6-4494579525a0.png)

You can also select a list *after* typing your task with the "in" keyword. To avoid false positives you will need to use all-caps in order to match a list by typing fewer than 3 characters.

#### Examples

> <strong>wl h:Fix the broken step saturday morning*</strong>
>
> ![wl h:Fix the broken step saturday morning*](https://cloud.githubusercontent.com/assets/507058/11939350/90d6001a-a7ef-11e5-9823-3273f611599c.png)
>
> **wl Buy clicky keyboard in shopping due sat**
>
> ![Buy clicky keyboard in sho due sat](https://cloud.githubusercontent.com/assets/507058/11939279/ffefa6f0-a7ee-11e5-9b7f-f5b1d55747a0.png)

> **wl Rearrange file cabinet tomorrow in WO**
>
> ![wl Rearrange file cabinet tomorrow in WO](https://cloud.githubusercontent.com/assets/507058/11939280/0244f108-a7ef-11e5-8d0d-726bb5e773d5.png)


### Reminders

Wunderlist uses alerts to remind you about tasks that are due, either on the due date or in advance. To set a reminder, either include a time with your due date or use an explicit reminder phrase like *remind me at 3:00pm on June 11*). 

#### Examples

> **wl Pay DoubleCash credit card bill monthly June 26th remind me June 22**
>
> ![wl Pay DoubleCash credit card bill monthly June 26th remind me June 22](https://cloud.githubusercontent.com/assets/507058/8271997/4779e33e-1800-11e5-91f4-55867bf1473a.png)
>
> **wl Make a New Year's resolution reminder: Jan 1 at midnight**
>
> ![wl Make a New Year's resolution reminder: Jan 1 at midnight](https://cloud.githubusercontent.com/assets/507058/8272030/c21fa028-1801-11e5-812a-fc66e4b9a232.png)
>
> **wl weekly meeting notes r 8am due 1d**
>
> ![wl weekly meeting notes r 8am due 1d](https://cloud.githubusercontent.com/assets/507058/8272020/5b49fd8a-1801-11e5-9d27-9851a8385bdc.png)
>
> **wl Laundry remind me**
>
> ![wl Laundry remind me](https://cloud.githubusercontent.com/assets/507058/8272070/6c15c502-1803-11e5-9a17-ed65b1a98f20.png)
>
> **wl Ask about app icon at dinner tomorrow**
>
> ![wl Ask about app icon at dinner tomorrow](https://cloud.githubusercontent.com/assets/507058/11858195/5593905a-a42d-11e5-8e66-9b27afb31f23.png)

#### When is the reminder?

You can set a custom default reminder time from the workflow preferences screen, otherwise when a time is not specified the reminder will be set for 9am.

|  Reminder phrase includes |           Task without due date            |               Task with due date               |
| ------------------------- | ------------------------------------------ | ---------------------------------------------- |
| **Time only**             | Reminder today at the specified time       | Reminder on the due date at the specified time |
| **Neither time nor date** | Today, 1 hour from the current time*       | Default time (9am) on the due date**            |
| **Date and time**         | Exact date and time entered                | Exact date and time entered                    |
| **Date only**             | Default time (9am) on the specified date** | Default time (9am) on the specified date**     |

\* By default, reminders for the current day will be set to 1 hour from the current time. You can change this offset in the workflow preferences.

\*\* The default time can be changed in the workflow preferences. If the specified date is today, your reminder date offset preference will be used instead.

### Due tasks

The `wl-due` command shows tasks that are due or overdue, similar to the Today list in Wunderlist. By default it hoists any recurring tasks that are *multiple times overdue* to the top, but you can change the sort order. Sadly, I have quite a few tasks that are multiple times overdue, so this features is mostly to keep me motivated but I hope others find it useful as well.



This view is searchable, just type to filter the results by keyword.

#### Sync before showing results

The due and upcoming screens will sync (or wait for the already-running sync) before showing results to make sure that everything is up-to-date. A notification is displayed if there is something to sync so that you're not waiting around too long without any feedback.

### Upcoming tasks

View upcoming tasks at `wl-upcoming`. It's kind of like the Week smart list in Wunderlist with the option to choose the duration that you prefer to look ahead (1 week, 2 weeks, 1 month, 3 days, whatever...). Like any other screen you can get there by typing as little as the first letter of the command: `wlu`:

![upcoming tasks](https://cloud.githubusercontent.com/assets/507058/17914990/9d5dbb88-6974-11e6-9fd4-592951703b09.png)

Browse or type to search your upcoming tasks. This screen can show upcoming tasks for any number of days with a few sensible defaults. Maybe there is someone out there who needs to see exactly 11 days ahead.

![upcoming duration](https://cloud.githubusercontent.com/assets/507058/17915036/2ce004b4-6975-11e6-8405-3793c005c21d.png)

### Search and browse tasks

The `wl-search` command allows you to search tasks by keyword or browse by list. To seach within a list, use the same *wl-search My List: some query* syntax as when entering a task.

#### Default search view
![search](https://cloud.githubusercontent.com/assets/507058/14915653/9e9716d6-0de2-11e6-8cc6-b098136752fd.png)

#### View a list
![view list](https://cloud.githubusercontent.com/assets/507058/13865584/3023b66c-ec83-11e5-936c-45950ed8bf4d.png)

#### Search within a list
![search list](https://cloud.githubusercontent.com/assets/507058/13865587/3bba2696-ec83-11e5-990f-890cb6eba9d1.png)

#### Search across all lists

Your search will match against tasks as well as list names.

![search](https://cloud.githubusercontent.com/assets/507058/13865628/a6fe572e-ec83-11e5-9d4f-4362178787bc.png)

#### Browse tasks by hashtag

Type the hash symbol # to view and select a tag.

![hashtags](https://cloud.githubusercontent.com/assets/507058/14915934/737bc60c-0de4-11e6-854d-fe1774d653e9.png)

### In sync

The workflow stays in sync with Wunderlist, so your lists (and tasks, in a later release) will be up-to-date and searchable. You can use the menu to select a list after typing the task. Just created a list in the Wunderlist app? No worries, it will show up in the workflow.

### Command shorthand

Commands like `wl:list` and `wl:pref` have been changed to `wl-list` and `wl-pref` to allow <kbd>Alt</kbd>+<kbd>delete</kbd> to return you to the welcome screen (any non-word character is fine, I just chose `-` for its word breaking properties). Furthermore, these commands can be triggered with as little as the first letter. `wld` will get you to the `wl-due` screen and `wls` will get you to `wl-search`. For this reason, you may noticed that top-level commands are first-letter-distinct to avoid conflicts.

### Hints

Read the text below each menu option and you'll be on your way to power user status – most menu items include helpful tips about how to apply a setting without navigating the menu.

If you notice any problems or want to see what changed in the latest version, jump to the *About* screen from the main menu or type `wl-about`. You will also find several preferences to customize the behavior of the workflow at `wl-pref` or the *Preferences* item on the welcome screen.

![Preferences](https://cloud.githubusercontent.com/assets/507058/18088801/a6d285c0-6e8a-11e6-8581-92ef0789dd34.png)

Security
--------

Your Wunderlist password is never made available to the workflow or stored in any way. Instead, when you log in through the Wunderlist portal you are asked to authorize the workflow to access your account. 

You can log out at any time through the `wl-pref` preferences screen. Upon logging out, all caches, synced data, and workflow preferences are removed. To revert to the default workflow settings simply log out then log back in.

Experimental updates
--------------------

Those who want to help test the newest features of the workflow can enable experimental updates in the `wl-pref` screen. When enabled, the workflow will prompt you to update to alpha and beta releases for the next major version. Note that these may be unstable and feedback is always appreciated if something goes wrong.

If you are currently using an experimental version the workflow will always prompt you to update to the latest experimental update regardless of this setting. Since fixes are common and often very important during this early stage of development it would not be good to allow old beta versions to continue misbehaving.

Limitations
-----------

* No offline mode – the workflow must be able to connect the the API for each change you make; currently changes made while offline are not saved.
* Languages and date formats – the workflow only officially supports US English at this time. parsedatetime provides US English, UK English, Dutch, German, Portuguese, Russian, and Spanish with varying coverage of keywords (e.g. tomorrow, Tuesday) in each language; your mileage may vary with these languages.

Contributing
------------

So you want to help make this workflow better? That's great! After cloning the repository, run `npm install && grunt` to build the workflow. Open the Wunderlist-symlinked.alfredworkflow file to install a copy in Alfred that will update whenever you rebuild the workflow. After making a change, simply run `grunt build` to update the workflow then use Alfred to test. Using this process, the workflow is kept up-to-date while you work.

Always run through the tests to ensure that your change does not cause issues elsewhere. When possible, add corresponding tests for your contributions.

Testing
-------

Unit tests are run automatically on every commit to reduce the likelihood of introducing a bug. Nevertheless, your feedback is crucial if anything seems to be broken.

Contributors can use the command `grunt test` to run the test suite and should do so to validate changes in any pull requests. If you add functionality, please back it with unit tests.

Acknowledgements
----------------

This workflow relies on the fantastic [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) by [Dean Jackson](https://github.com/deanishe) to communicate with Alfred. The Alfred-Workflow library source code is bundled with the workflow and also included with the repository as a submodule.

Much of the natural language date processing is powered by [parsedatetime](https://github.com/bear/parsedatetime), a tremendously powerful date parser built by [Mike Taylor](https://github.com/bear) and various contributors. [Peewee](https://github.com/coleifer/peewee) by [Charles Leifer](https://github.com/coleifer) provides a simple interface to store and query synced data retrieved from Wunderlist using [Requests](https://github.com/kennethreitz/requests) by [Kenneth Reitz](https://github.com/kennethreitz). The source code of all three libraries is bundled with the workflow and each is included in the repository as a submodule.

Alternatives
------------

* Wunderlist itself! The 6Wunderkinder team has been incorporating many of the features found in this workflow directly into the app so that you can enjoy the convenience of natural language due dates and reminders across all platforms.
