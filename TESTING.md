Testing the Wunderlist Workflow
===============================

The following test cases are intended to provide adequate coverage while maintaining ease of testing. Each release must be tested to ensure compliance with each of the tests and to avoid reintroducing bugs. While it may be possible to automate these tests in the future, currently that is outside of the scope of this project.

Automated Tests
---------------

This workflow now includes a semi-automated testing procedure stepping through each of these tests with the option to run all or individual tests. Each test provides instructions for proper setup before running the test (such as making sure Wunderlist is running on a different desktop) as well as intructions to manually verify whether the test passed or failed. 

At this time it is not within the scope of this project to automatically verify test results as this would require implementation of a lot of features that are not needed for normal operation of the workflow. Once Wunderlist supports AppleScript, that can be expected to change!

To run the automated tests, simply execute `./run_tests.sh` from the project's root directory. Without arguments, all tests will be run. Alternatively, any number of tests can be specified to run specific tests or suites. For example you could run all tests in the *Go to a list* suite with `./run_tests.sh 2` or run all Unicode-related test with `./run_tests.sh 1.0.1 1.2.1 3.0.1`. At the start of each test, simply press *Cancel* to end the test run early.

Adding Tasks
------------

#### Adding a task to the Inbox

**Test 1.0.0 –** Simple `wlin` task <a name="1.0.0"></a>

|         Action        |    Alfred Query    | Alfred Results |                  Wunderlist                 |
| --------------------- | ------------------ | -------------- | ------------------------------------------- |
| Type `wlin` in Alfred | `wlin`             | *Inbox*        | —                                           |
| Type ` Sample task`   | `wlin Sample task` | *Inbox*        | —                                           |
| Press *return*        | —                  | —              | New task *Sample task* added in the *Inbox* |

-----

**Test 1.0.1 –** Unicode and character escaping in `wlin` <a name="1.0.1"></a>

|            Action            |         Alfred Query        | Alfred Results |                      Wunderlist                      |
| ---------------------------- | --------------------------- | -------------- | ---------------------------------------------------- |
| Type `wlin` in Alfred        | `wlin`                      | *Inbox*        | —                                                    |
| Type ` Sámple \/][;$ "task"` | `wlin Sámple \/][;$ "task"` | *Inbox*        | —                                                    |
| Press *return*               | —                           | —              | New task *Sámple \/][;$ "task"* added in the *Inbox* |


#### Adding a task to a list by autocompletion

**Test 1.1.0 –** Simple `wl` task with autocompletion <a name="1.1.0"></a>

|         Action         |       Alfred Query       |          Alfred Results          |                Wunderlist               |
| ---------------------- | ------------------------ | -------------------------------- | --------------------------------------- |
| Type `wl to` in Alfred | `wl to`                  | *Today* and other matching lists | —                                       |
| Press *tab*            | `wl Today:`              | *Today*                          | —                                       |
| Type ` Sample task`    | `wlin Today:Sample task` | *Today*                          | —                                       |
| Press *return*         | —                        | —                                | New task *Sample task* added in *Today* |


#### Adding a task to a list by substring matching

**Test 1.2.0 –** Simple `wl` task with substring matching <a name="1.2.0"></a>

|          Action         |     Alfred Query    |          Alfred Results          |                Wunderlist                |
| ----------------------- | ------------------- | -------------------------------- | ---------------------------------------- |
| Type `wl to:` in Alfred | `wl to:`            | *Today* and other matching lists | —                                        |
| Type `Sample task`      | `wl to:Sample task` | *Today* and other matching lists | —                                        |
| Press *return*          | —                   | —                                | New task *Sample task* added in *Today*  |

-----

**Test 1.2.1 –** Unicode and character escaping in `wl` <a name="1.2.1"></a>

|                    Action                   |         Alfred Query         |          Alfred Results          |                    Wunderlist                    |
| ------------------------------------------- | ---------------------------- | -------------------------------- | ------------------------------------------------ |
| Type `wl to:Sámple \/][;$ "task"` in Alfred | `wl to:Sámple \/][;$ "task"` | *Today* and other matching lists | —                                                |
| Press *return*                              | —                            | —                                | New task *Sámple \/][;$ "task"* added in *Today* |

-----

**Test 1.2.2 –** `wl` task containing a colon <a name="1.2.2"></a>

|         Action        |    Alfred Query   |            Alfred Results           |                          Wunderlist                          |
| --------------------- | ----------------- | ----------------------------------- | ------------------------------------------------------------ |
| Type `wl S` in Alfred | `wl S`            | Any lists containing the letter *s* | —                                                            |
| Type `ample: task`    | `wl Sample: task` | All lists with most recent on top   | —                                                            |
| Press *return*        | —                 | —                                   | New task *Sample: task* added in the most recently used list |

-----

**Test 1.2.3 –** `wl` task containing a colon with substring matching <a name="1.2.3"></a>

|          Action         |     Alfred Query     |          Alfred Results          |                Wunderlist                |
| ----------------------- | -------------------- | -------------------------------- | ---------------------------------------- |
| Type `wl to:` in Alfred | `wl to:`             | *Today* and other matching lists | —                                        |
| Type `Sample: task`     | `wl to:Sample: task` | *Today* and other matching lists | —                                        |
| Press *return*          | —                    | —                                | New task *Sample: task* added in *Today* |

#### Adding a task to a list by selecting the list

**Test 1.3.0 –** Simple `wl` task by selecting the list <a name="1.3.0"></a>

|                    Action                    |   Alfred Query   |           Alfred Results          |                Wunderlist               |
| -------------------------------------------- | ---------------- | --------------------------------- | --------------------------------------- |
| Type `wl Sample task` in Alfred              | `wl Sample task` | All lists with most recent on top | —                                       |
| Press *down arrow* until *Today* is selected | `wl Sample task` | Same lists with *Today* selected  | —                                       |
| Press *return*                               | —                | —                                 | New task *Sample task* added in *Today* |

-----

**Test 1.3.1 –** Simple `wl` task in most recently used list <a name="1.3.1"></a>

|              Action             |   Alfred Query   |           Alfred Results          |                          Wunderlist                         |
| ------------------------------- | ---------------- | --------------------------------- | ----------------------------------------------------------- |
| Type `wl Sample task` in Alfred | `wl Sample Task` | All lists with most recent on top | —                                                           |
| Press *return*                  | —                | —                                 | New task *Sample task* added in the most recently used list |

-----

**Test 1.3.2 –** `wl` task prefixed by a colon <a name="1.3.2"></a>

|                    Action                    |    Alfred Query   |           Alfred Results          |                Wunderlist               |
| -------------------------------------------- | ----------------- | --------------------------------- | --------------------------------------- |
| Type `wl :Sample task` in Alfred             | `wl :Sample task` | All lists with most recent on top | —                                       |
| Press *down arrow* until *Today* is selected | `wl :Sample task` | Same lists with *Today* selected  | —                                       |
| Press *return*                               | —                 | —                                 | New task *Sample task* added in *Today* |
|                                              |                   |                                   |                                         |

#### Wunderlist window modes

**Test 1.4.0 –** Adding a task with Wunderlist in compact mode <a name="1.4.0"></a>

|                     Action                     |     Alfred Query    |          Alfred Results          |                Wunderlist               |
| ---------------------------------------------- | ------------------- | -------------------------------- | --------------------------------------- |
| Select *Window* > *Compact Mode* in Wunderlist | —                   | —                                | Wunderlist is in Compact mode           |
| Type `wl to:Sample task` in Alfred             | `wl to:Sample task` | *Today* and other matching lists | —                                       |
| Press *return*                                 | —                   | —                                | Wunderlist switches to Normal mode      |
|                                                |                     |                                  | New task *Sample task* added in *Today* |

-----

**Test 1.4.1 –** Adding a task with Wunderlist window closed <a name="1.4.1"></a>

|                         Action                        |     Alfred Query    |            Alfred Results            |                    Wunderlist                    |
| ----------------------------------------------------- | ------------------- | ------------------------------------ | ------------------------------------------------ |
| Activate Wunderlist                                   | –                   | –                                    | Any Wunderlist window is visible                 |
| Press *Cmd+W* to close the window                     | –                   | –                                    | Wunderlist has no visible window                 |
| Activate an app on the **same** desktop as Wunderlist | —                   | —                                    | –                                                |
| Type `wl to:Sample task` in Alfred                    | `wl to:Sample task` | *Today* and any other matching lists | –                                                |
| Press *return*                                        | –                   | –                                    | New task "Sample task" added in the *Today* list |
| Wait a few seconds                                    | —                   | —                                    | Previous frontmost application is reactivated    |

-----

**Test 1.4.2 –** Adding a task with Wunderlist window minimized and built-in list selected <a name="1.4.2"></a>

|                         Action                        |     Alfred Query    |            Alfred Results            |                    Wunderlist                    |
| ----------------------------------------------------- | ------------------- | ------------------------------------ | ------------------------------------------------ |
| Activate Wunderlist                                   | –                   | –                                    | Any Wunderlist window is visible                 |
| Select the *Today* list                               | –                   | –                                    | *Today* list is selected                         |
| Press *Cmd+M* to minimize the window                  | –                   | –                                    | Wunderlist window is minimized                   |
| Activate an app on the **same** desktop as Wunderlist | —                   | —                                    | –                                                |
| Type `wl to:Sample task` in Alfred                    | `wl to:Sample task` | *Today* and any other matching lists | –                                                |
| Press *return*                                        | –                   | –                                    | New task "Sample task" added in the *Today* list |
| Wait a few seconds                                    | —                   | —                                    | Previous frontmost application is reactivated    |

-----

**Test 1.4.3 –** Adding a task with Wunderlist window minimized and custom list selected <a name="1.4.3"></a>

|                         Action                        |     Alfred Query    |            Alfred Results            |                    Wunderlist                    |
| ----------------------------------------------------- | ------------------- | ------------------------------------ | ------------------------------------------------ |
| Activate Wunderlist                                   | –                   | –                                    | Any Wunderlist window is visible                 |
| Select any custom list                                | –                   | –                                    | A custom list is selected                        |
| Press *Cmd+M* to minimize the window                  | –                   | –                                    | Wunderlist window is minimized                   |
| Activate an app on the **same** desktop as Wunderlist | —                   | —                                    | –                                                |
| Type `wl to:Sample task` in Alfred                    | `wl to:Sample task` | *Today* and any other matching lists | –                                                |
| Press *return*                                        | –                   | –                                    | New task "Sample task" added in the *Today* list |
| Wait a few seconds                                    | —                   | —                                    | Previous frontmost application is reactivated    |

-----

**Test 1.4.4 –** Adding a task with Wunderlist not yet running <a name="1.4.4"></a>

|               Action               |     Alfred Query    |            Alfred Results            |                              Wunderlist                             |
| ---------------------------------- | ------------------- | ------------------------------------ | ------------------------------------------------------------------- |
| Quit Wunderlist                    | –                   | –                                    | Wunderlist is not running                                           |
| Type `wl to:Sample task` in Alfred | `wl to:Sample task` | *Today* and any other matching lists | –                                                                   |
| Press *return*                     | –                   | –                                    | Wunderlist starts, new task "Sample task" added in the *Today* list |
| Wait a few seconds                 | —                   | —                                    | Previous frontmost application is reactivated                       |


Go to a List
------------

#### Go to list by autocompletion

**Test 2.0.0 –** Go to list by autocompletion <a name="2.0.0"></a>

|         Action         | Alfred Query |          Alfred Results          |                Wunderlist                |
| ---------------------- | ------------ | -------------------------------- | ---------------------------------------- |
| Type `wl to` in Alfred | `wl to`      | *Today* and other matching lists | —                                        |
| Press *tab*            | `wl Today:`  | *Today*                          | —                                        |
| Press *return*         | —            | —                                | *Today* list is selected                 |
| Wait a few seconds     | —            | —                                | Wunderlist remains frontmost application |


#### Go to list by substring matching

**Test 2.1.0 –** Go to list by substring matching <a name="2.1.0"></a>

|          Action         | Alfred Query |          Alfred Results          |                Wunderlist                |
| ----------------------- | ------------ | -------------------------------- | ---------------------------------------- |
| Type `wl to:` in Alfred | `wl to:`     | *Today* and other matching lists | —                                        |
| Press *return*          | —            | —                                | *Today* list is selected                 |
| Wait a few seconds      | —            | —                                | Wunderlist remains frontmost application |


#### Go to *Inbox* by `wlin`

**Test 2.2.0 –** Go to *Inbox* by `wlin` <a name="2.2.0"></a>

|         Action        | Alfred Query | Alfred Results |                Wunderlist                |
| --------------------- | ------------ | -------------- | ---------------------------------------- |
| Type `wlin` in Alfred | `wlin`       | *Inbox*        | —                                        |
| Press *return*        | —            | —              | *Inbox* list is selected                 |
| Wait a few seconds    | —            | —              | Wunderlist remains frontmost application |



Adding Lists
------------

#### Add a new list

**Test 3.0.0 –** Add a new list <a name="3.0.0"></a>

|                Action               |     Alfred Query     | Alfred Results |          Wunderlist          |
| ----------------------------------- | -------------------- | -------------- | ---------------------------- |
| Type `wllist Sample list` in Alfred | `wllist Sample list` | New list       | —                            |
| Press *return*                      | —                    | —              | New list *Sample list* added |

-----

**Test 3.0.1 –** Unicode and character escaping in `wllist` <a name="3.0.1"></a>

|                    Action                    |          Alfred Query         | Alfred Results |               Wunderlist              |
| -------------------------------------------- | ----------------------------- | -------------- | ------------------------------------- |
| Type `wllist Sámple \/][;$ "list"` in Alfred | `wllist Sámple \/][;$ "list"` | New list       | —                                     |
| Press *return*                               | —                             | —              | New list *Sámple \/][;$ "list"* added |


#### New list appears in `wl` command

**Test 3.1.0 –** Newly added list appears in `wl` command <a name="3.1.0"></a>

|                Action               |     Alfred Query     |           Alfred Results          |          Wunderlist          |
| ----------------------------------- | -------------------- | --------------------------------- | ---------------------------- |
| Type `wllist Sample list` in Alfred | `wllist Sample list` | New list                          | —                            |
| Press *return*                      | —                    | —                                 | New list *Sample list* added |
| Type `wl` in Alfred                 | `wl`                 | All lists including *Sample list* | —                            |


#### Wunderlist window modes

**Test 3.2.0 –** Adding a list with Wunderlist in compact mode <a name="3.2.0"></a>

|                     Action                     |     Alfred Query    | Alfred Results |             Wunderlist             |
| ---------------------------------------------- | ------------------- | -------------- | ---------------------------------- |
| Select *Window* > *Compact Mode* in Wunderlist | —                   | —              | Wunderlist is in Compact mode      |
| Type `wllist Sample list` in Alfred            | `wllist Sample list | New list       | —                                  |
| Press *return*                                 | —                   | —              | Wunderlist switches to Normal mode |
|                                                |                     |                | New list *Sample list* added       |

-----

**Test 3.2.1 –** Adding a list with Wunderlist window closed <a name="3.2.1"></a>

|                         Action                        |     Alfred Query    | Alfred Results |            Wunderlist            |
| ----------------------------------------------------- | ------------------- | -------------- | -------------------------------- |
| Activate Wunderlist                                   | –                   | –              | Any Wunderlist window is visible |
| Press *Cmd+W* to close the window                     | –                   | –              | Wunderlist has no visible window |
| Activate an app on the **same** desktop as Wunderlist | —                   | —              | –                                |
| Type `wllist Sample list` in Alfred                   | `wllist Sample list | New list       | —                                |
| Press *return*                                        | —                   | —              | Wunderlist window opens          |
|                                                       |                     |                | New list *Sample list* added     |

-----

**Test 3.2.2 –** Adding a list with Wunderlist window minimized <a name="3.2.2"></a>

|                         Action                        |     Alfred Query    | Alfred Results |            Wunderlist            |
| ----------------------------------------------------- | ------------------- | -------------- | -------------------------------- |
| Activate Wunderlist                                   | –                   | –              | Any Wunderlist window is visible |
| Press *Cmd+M* to minimize the window                  | –                   | –              | Wunderlist window is minimized   |
| Activate an app on the **same** desktop as Wunderlist | —                   | —              | –                                |
| Type `wllist Sample list` in Alfred                   | `wllist Sample list | New list       | —                                |
| Press *return*                                        | —                   | —              | Wunderlist window opens          |
|                                                       |                     |                | New list *Sample list* added     |

-----

**Test 3.2.3 –** Adding a list with Wunderlist viewing search results <a name="3.2.3"></a>

|                         Action                        |     Alfred Query    | Alfred Results |                   Wunderlist                  |
| ----------------------------------------------------- | ------------------- | -------------- | --------------------------------------------- |
| Activate Wunderlist                                   | –                   | –              | Any Wunderlist window is visible              |
| Press *Cmd+F* to search, type "sample"                | –                   | –              | Wunderlist is showing tasks matching "sample" |
| Activate an app on the **same** desktop as Wunderlist | —                   | —              | –                                             |
| Type `wllist Sample list` in Alfred                   | `wllist Sample list | New list       | —                                             |
| Press *return*                                        | —                   | —              | Wunderlist window opens                       |
|                                                       |                     |                | New list *Sample list* added                  |


Navigation Between Apps
-----------------------

#### Switching back to the previous application

**Test 4.0.0 –** Switching back to previous application on the same desktop <a name="4.0.0"></a>

|                         Action                        |    Alfred Query    | Alfred Results |                    Wunderlist                    |
| ----------------------------------------------------- | ------------------ | -------------- | ------------------------------------------------ |
| Activate an app on the **same** desktop as Wunderlist | —                  | —              | —                                                |
| Type `wlin Sample task` in Alfred                     | `wlin Sample task` | *Inbox*        | —                                                |
| Press *return*                                        | —                  | —              | New task "Sample task" added in the *Inbox* list |
| Wait a few seconds                                    | —                  | —              | Previous frontmost application is reactivated    |

-----

**Test 4.0.1 –** Switching back to previous application on a different desktop <a name="4.0.1"></a>

|                           Action                           |    Alfred Query    | Alfred Results |                    Wunderlist                    |
| ---------------------------------------------------------- | ------------------ | -------------- | ------------------------------------------------ |
| Right-click the Wunderlist icon in the dock                | —                  | —              | —                                                |
| Select *Options* > *Assign To* > *None*                    | —                  | —              | —                                                |
| Activate an app on a **different** desktop than Wunderlist | —                  | —              | —                                                |
| Type `wlin Sample task` in Alfred                          | `wlin Sample task` | *Inbox*        | —                                                |
| Press *return*                                             | —                  | —              | New task "Sample task" added in the *Inbox* list |
| Wait a few seconds                                         | —                  | —              | Previous frontmost application is reactivated    |


Checklist Template
------------------

Use this template for confirming test compliance on each release

```
- [ ] **Test 1.0.0 –** Simple `wlin` task
- [ ] **Test 1.0.1 –** Unicode and character escaping in `wlin`
- [ ] **Test 1.1.0 –** Simple `wl` task with autocompletion
- [ ] **Test 1.2.0 –** Simple `wl` task with substring matching
- [ ] **Test 1.2.1 –** Unicode and character escaping in `wl`
- [ ] **Test 1.2.2 –** `wl` task containing a colon
- [ ] **Test 1.2.3 –** `wl` task containing a colon with substring matching
- [ ] **Test 1.3.0 –** Simple `wl` task by selecting the list
- [ ] **Test 1.3.1 –** Simple `wl` task in most recently used list
- [ ] **Test 1.3.2 –** `wl` task prefixed by a colon
- [ ] **Test 2.0.0 –** Go to list by autocompletion
- [ ] **Test 2.1.0 –** Go to list by substring matching
- [ ] **Test 2.2.0 –** Go to *Inbox* by `wlin`
- [ ] **Test 3.0.0 –** Add a new list
- [ ] **Test 3.0.1 –** Unicode and character escaping in `wllist`
- [ ] **Test 3.1.0 –** Newly added list appears in `wl` command
- [ ] **Test 4.0.0 –** Switching back to previous application on the same desktop
- [ ] **Test 4.0.1 –** Switching back to previous application on a different desktop
- [ ] **Test 4.1.0 –** Adding a task with Wunderlist window closed
- [ ] **Test 4.2.0 –** Adding a task with Wunderlist window minimized and built-in list selected
- [ ] **Test 4.2.1 –** Adding a task with Wunderlist window minimized and custom list selected
```