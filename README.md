Wunderlist Workflow for Alfred
==========================

Create tasks in [Wunderlist](http://wunderlist.com) more effortlessly than ever before with this [Alfred 2](http://www.alfredapp.com/) workflow (requires Powerpack license). 

Beginner and advanced approaches to adding a monthly repeating task beginning the following week:

![Simple and advanced usage](https://cloud.githubusercontent.com/assets/507058/7975455/ff5acaea-0a3b-11e5-93f9-74b4b14039dc.gif)

Setup
-----

### [Download here](https://raw.github.com/idpaterson/alfred-wunderlist-workflow/master/Wunderlist.alfredworkflow)

After downloading, simply double-click to install the workflow in Alfred. Use the `wl` command in Alfred to activate the workflow, or assign a hotkey in Alfred preferences. The workflow will guide you through securely logging in to Wunderlist and will even let you know when an important update is available.

Features you'll love
--------

The workflow provides an easy guided experience with tips along the way that will help you become a power user. 

The welcome screen appears when you've typed `wl` (and nothing else). Special commands are in the form `wl:command` with no space; once you type a space after `wl ` you're in task entry mode (at least for now, this is a bit harsh).

![Welcome screen](https://cloud.githubusercontent.com/assets/507058/11870946/fffcff2e-a499-11e5-8528-5cfa0778dfed.png)


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

> <strong>wl h:Fix the broken step saturday morning*</strong><br/>
![wl h:Fix the broken step saturday morning*](https://cloud.githubusercontent.com/assets/507058/11939350/90d6001a-a7ef-11e5-9823-3273f611599c.png)

> **wl Buy clicky keyboard in shopping due sat**<br/>
![Buy clicky keyboard in sho due sat](https://cloud.githubusercontent.com/assets/507058/11939279/ffefa6f0-a7ee-11e5-9b7f-f5b1d55747a0.png)

> **wl Rearrange file cabinet tomorrow in WO**<br/>
![wl Rearrange file cabinet tomorrow in WO](https://cloud.githubusercontent.com/assets/507058/11939280/0244f108-a7ef-11e5-8d0d-726bb5e773d5.png)


### Reminders

Wunderlist uses alerts to remind you about tasks that are due, either on the due date or in advance. To set a reminder, either include a time with your due date or use an explicit reminder phrase like *remind me at 3:00pm on June 11*). 

#### Examples

> **wl Pay DoubleCash credit card bill monthly June 26th remind me June 22**<br/>
![wl Pay DoubleCash credit card bill monthly June 26th remind me June 22](https://cloud.githubusercontent.com/assets/507058/8271997/4779e33e-1800-11e5-91f4-55867bf1473a.png)

> **wl Make a New Year's resolution reminder: Jan 1 at midnight**<br/>
![wl Make a New Year's resolution reminder: Jan 1 at midnight](https://cloud.githubusercontent.com/assets/507058/8272030/c21fa028-1801-11e5-812a-fc66e4b9a232.png)

> **wl weekly meeting notes r 8am due 1d**<br/>
![wl weekly meeting notes r 8am due 1d](https://cloud.githubusercontent.com/assets/507058/8272020/5b49fd8a-1801-11e5-9d27-9851a8385bdc.png)

> **wl Laundry remind me**<br/>
![wl Laundry remind me](https://cloud.githubusercontent.com/assets/507058/8272070/6c15c502-1803-11e5-9a17-ed65b1a98f20.png)

> **wl Ask about app icon at dinner tomorrow**<br/>
![wl Ask about app icon at dinner tomorrow](https://cloud.githubusercontent.com/assets/507058/11858195/5593905a-a42d-11e5-8e66-9b27afb31f23.png)

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

### In sync

The workflow stays in sync with Wunderlist, so your lists (and tasks, in a later release) will be up-to-date and searchable. You can use the menu to select a list after typing the task. Just created a list in the Wunderlist app? No worries, it will show up in the workflow.

### Hints

Read the text below menu option and you'll be on your way to power user status – most menu items include helpful tips about how to apply a setting without navigating the menu.

If you notice any problems or want to see what changed in the latest version, jump to the *About* screen from the main menu or type `wl:about`. You will also find several preferences to customize the behavior of the workflow at `wl:pref` or the *Preferences* item on the welcome screen.

![Preferences](https://cloud.githubusercontent.com/assets/507058/11939113/c132fd14-a7ed-11e5-8fd1-9e3727acee26.png)


Security
-----------

Your Wunderlist password is never made available to the workflow or stored in any way. Instead, when you log in through the Wunderlist portal you are asked to authorize the workflow to access your account. 

You can log out at any time through the `wl:pref` preferences screen. Upon logging out, all caches, synced data, and workflow preferences are removed. To revert to the default workflow settings simply log out then log back in.

Limitations
-----------

* No offline mode – the workflow must be able to connect the the API for each change you make; currently changes made while offline are not saved.
* Languages and date formats – the workflow only officially supports US English at this time. parsedatetime provides US English, UK English, Spanish, German, and Dutch with varying coverage of keywords (e.g. tomorrow, Tuesday) in each language; your mileage may vary with these languages. It is possible to add support for any local date format or language by installing some extra software, but there are a number of outstanding issues with adapting to generic locales.

Contributing
------------

So you want to help make this workflow better? That's great! After cloning the repository, run `npm install && grunt` to build the workflow. Open the Wunderlist-symlinked.alfredworkflow file to install a copy in Alfred that will update whenever you rebuild the workflow. After making a change, simply run `grunt build` to update the workflow then use Alfred to test. Using this process, the workflow is kept up-to-date while you work.

Always run through the semi-automated tests to ensure that your change does not cause issues elsewhere. When possible, add corresponding tests for your contributions.

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
* [Wunderlist-3-Alfred](https://github.com/camgnostic/Wunderlist-3-Alfred) by [camgnostic](https://github.com/camgnostic)
