(*!
	@header     Wunderlist for Alfred
	@abstract   Control Wunderlist 2 from Alfred
	@discussion This AppleScript provides a means to control the Wunderlist 2 Mac app from Alfred.
	            As Wunderlist 2 does not yet provide AppleScript support, the features are limited
	            to those that are keyboard-accessible. Regardless, it saves a lot of keystrokes!
	@author     Ian Paterson
	@version    0.1
*)

(*! 
	@group Configuration
*)

(*!
	Determines which color theme to use for the list icons. These
	icons 

	@abstract Changes the appearance of list icons in Alfred
	@attributelist Supported Values
		light For use in dark-colored Alfred themes
		dark  For use in light-colored Alfred themes
*)
property iconTheme : "light"

(*!
	The list of tasks available in Wunderlist is cached by this workflow,
	enabling faster responses to typing in Script Filter inputs. This
	setting controls how often the cached list data is refreshed.

	@abstract Specifies how often to reload information about task lists
*)
property listCacheInSeconds : 30


(*! 
	@functiongroup Interaction with Wunderlist
*)

# Keep track of the current app
property originalApp : missing value

# The path to this workflow within Alfred's preferences bundle
property workflowFolder : missing value

# The qWorkflow script loaded into memory as necessary
property qWorkflowScript : missing value

(*! 
	@abstract Causes Wunderlist to become the active application.
*)
on activateWunderlist()
	
	# Ensure we can return to the current active application later
	set originalApp to path to frontmost application as text

	activate application "Wunderlist"
	
end activateWunderlist

(*! 
	@abstract  Activates the original <code>frontmost application</code> 
	before the script was started.
*)
on activatePreviousApplication()
	
	activate application originalApp
	
end activatePreviousApplication

(*! 
	@abstract  Uses the Dock.app menu to make Wunderlist visible on all
	desktops, which is necessary for the list info to load reliably.
*)
on assignWunderlistToAllDesktops()

	set optionsMenu to appl10n("OPTIONS", "Dock", "DockMenus")
	set allDesktopsMenuItem to appl10n("ALL_DESKTOPS", "Dock", "DockMenus")

	tell application "System Events" 
		tell UI element "Wunderlist" of list 1 of process "Dock"

			# Show the context menu for the Wunderlist dock icon
			perform action "AXShowMenu"
			click menu item optionsMenu of menu 1
			click menu item allDesktopsMenuItem of menu 1 of menu item optionsMenu of menu 1

		end tell
	end tell

end assignWunderlistToAllDesktops

(*!
	@abstract   Launches the Wunderlist application if it is not already
	running and waits for it to load.
	@discussion If Wunderlist is running but is not located on the current
	desktop, it would not be possible to query the list info from the app's
	UI. When this occurs, @link assignWunderlistToAllDesktops() @/link will
	be used to bring Wunderlist to the current desktop and ensure that it
	is always available.
*)
on launchWunderlistIfNecessary()

	set appName to "Wunderlist"
	
	tell application "System Events"
		set wunderlistIsRunning to (name of processes) contains appName
	end tell

	# Wunderlist has to be running, if not 
	if not wunderlistIsRunning then
		tell application appName to launch

		# Wait for application to launch
		tell application "System Events"
			repeat until count of windows of process appName > 0
				delay 0.05
			end repeat
		end tell
	end if

	try 
		tell application "System Events" to get window appName of process appName
	on error
		# Wunderlist is not on the current desktop. Use this opportunity to
		# assign it.
		assignWunderlistToAllDesktops()

		# Tell the user what just happened. Unfortunately they're going to have to
		# start their Alfred query again.
		sendNotification("Messages/Wunderlist is now on all desktops")
	end try

end launchWunderlistIfNecessary

(*!
	@abstract   Moves focus within the app to the Inbox list.
	@discussion Uses the keyboard to move focus within the app to the Inbox list. 
	The Inbox list is a good reference point because it is always at the top of the 
	lists table.

	The procedure for accessing the Inbox from any point in the app is as follows:
	1. <code>⌘+f</code> Begin a search
	2. Perform a search that will probably not return results and will not be too 
	distracting. 3 space characters works fine.
	3. <code>⌘+n</code> Navigate to the Inbox, focused on the Inbox list
*)
on focusInbox()
	
	tell application "System Events"
		
		# Begin a search, simply because it's the easiest 
		# programmatic avenue to the Inbox
		keystroke "f" using command down
		
		delay 0.1
		
		# Search for an arbitrary string. 
		# Wunderlist will not return any results, so visually this
		# just looks like a transition between lists
		keystroke "   "
		
		# Search takes a moment
		delay 0.5
		
		# Once in a search, Command-N activates the Inbox
		keystroke "n" using command down
		
		delay 0.1
		
	end tell

end focusInbox


(*!
	@abstract   Moves focus within the app to the specified list.
	@discussion After calling focusInbox as a reference, simply use the 
	arrow keys to move focus to the desired list.

	The procedure for focusing a specific list is as follows:
	1. Focus the Inbox list
	2. Press the down arrow as necessary until the list is focused

	@param listIndex The numerical one-based index of the desired list.
*)
on focusListAtIndex(listIndex)
	
	focusInbox()
	
	tell application "System Events"
		
		repeat listIndex - 1 times
			
			# Down arrow to go to the next list
			key code 125
			
		end repeat
		
	end tell
	
end focusListAtIndex


(*!
	@abstract   Returns focus to the last list viewed prior to navigating lists.
	@discussion Conveniently, Wunderlist goes back to the previously viewed task when the
	search term is cleared. This means that we can call @link focusInbox @/link
	or even @link focusListAtIndex @/link, add tasks, and then go return 
	Wunderlist to its original view state.

	The procedure for returning to the previous list is as follows:
	1. <code>⌘+f</code> Return to the search input
	2. Press the delete key to clear the search, Wunderlist will switch back to the previously viewed list
	3. <code>⌘+n</code> Move focus out of the search box into the task list
	4. <code>⇧+tab</code> Return focus to the list table
*)
on focusPreviousList()
	
	tell application "System Events"
		
		# Back to the search box, which will highlight the existing text
		keystroke "f" using command down
		
		# Delete key to clear the search query
		# Best thing is, this sends Wunderlist back to whichever list 
		# was focused before the original search
		key code 51
		
		# Move focus from the search field to the task input
		keystroke "n" using command down
		
		# Focus on the list for easy keyboard navigation
		keystroke tab using shift down
		
	end tell
	
end focusPreviousList


(*!
	@abstract   Switches keyboard focus to the task input field.
	@discussion In certain views it is necessary to use the New Task shortcut twice
	because the first time switches the UI to the Inbox list.

	The procedure for returning to the previous list is as follows:
	1. <code>⌘+n</code> Focus the task input, or in some cases focus the Inbox
	2. <code>⌘+n</code> For good measure in case the previous command focused the Inbox
*)
on focusTaskInput()
	
	tell application "System Events"
		
		# Focus task input to create a new task
		# If searching, Command-N is required twice to create a task
		keystroke "n" using command down
		keystroke "n" using command down
		
	end tell
	
end focusTaskInput

(*!
	@abstract Switches to the "Normal" view in Wunderlist where both the list and 
	tasks are visible.
*)
on setWindowViewNormal()
	
	tell application "System Events"
		
		# Make sure Wunderlist is in Normal View
		keystroke "1" using command down
		
	end tell
	
end setWindowViewNormal


(*!
	@abstract Loads some basic information about all of the visible lists in Wunderlist.
	@discussion Wunderlist exposes a small amount of information about the tasks that
	can be retrieved by traversing the UI. This information includes the name of each
	list and its number of tasks.

	Unfortunately, the number of tasks returned is undefined when there are no tasks in 
	a list. Wunderlist does not set the value of the task count label to zero, nor does
	it hide the label in a way that is detectable by AppleScript. The value in the label
	appears to change in an undefined way, so unfortunately at this time the task
	count is unreliable.

	@return A list of records in the <code>ListInfo</code> format described below
	@attributeList <code>ListInfo</code> record
		<code>listName</code>  The display name of the list
		<code>taskCount</code> The number of uncompleted tasks in the list
	    <code>listIndex</code> The one-based index of the list
*)
on getListInfo()

	tell application "System Events"
		tell process "Wunderlist"
			# The immediate parent element of all the list elements
			set listsContainer to UI element 1 of UI element 1 of UI element 1 of UI element 1 of splitter group 1 of window "Wunderlist"
			
			set listValues to value of static texts of UI elements of listsContainer
			
			set listInfo to {}
			set listIndex to 0
			
			repeat with listValue in listValues
				if (count of listValue) is 2 then
					# There are a few elements in addition to the list elements,
					# but the list elements are easily identifiable as those having 
					# 2 children.
					set {listName, taskCount} to listValue
					
					set listIndex to listIndex + 1
					set taskCount to taskCount as integer
					
					set listInfo to listInfo & {{listName:listName, taskCount:taskCount, listIndex:listIndex}}
				end if
				
			end repeat
			
			return listInfo
		end tell
	end tell
	
end getListInfo

(*!
	@abstract   Retrieves cached list info or loads the list data again if necessary
	@discussion The list info is cached as specified by @link listCacheInSeconds @/link
	to optimize repetitive access of the list, as with an Alfred Script Filter.

	The keys <code>lists</code> and <code>listsUpdatedDate</code> in the default
	<code>settings.plist</code> are used to track the lists state.
	@see getListInfo
	@param wf The qWorkflow workflow object for this script
	@return A list of <code>ListValue</code> records
*)
on getListInfoInWorkflow(wf)

	# Load the list info and the cache date
	set listInfo to wf's get_value("lists", "")
	set lastUpdatedDate to wf's get_value("listsUpdatedDate", "")

	# Reload the list info if the cached data is missing or expired
	if lastUpdatedDate is missing value or current date - lastUpdatedDate > listCacheInSeconds then
		set listInfo to getListInfo()

		wf's set_value("lists", listInfo, "")
		wf's set_value("listsUpdatedDate", current date, "")
	end if

	return listInfo

end getListInfoInWorkflow

(*!
	@abstract   Finds the index of the specified list in the list table
	@discussion Returns a one-based index of the list with the specified name,
	or <code>missing value</code> if the list does not exist

	@param theListName Text exactly matching the name of a list
	@return The integer index or <code>missing value</code> if no list with
	the specified name exists
*)
on getIndexOfListNamed(theListName)

	set listInfo to getListInfo()

	# Find the matching list
	repeat with i from 1 to count of listInfo
		if listName of item i of listInfo is theListName
			return i
		end 
	end repeat

	return missing value

end getIndexOfListNamed

(*!
	@abstract   Loads info about the tasks in the currently visible task list
	@discussion Loads some basic information about all of the items in the visible 
	list in Wunderlist. Unfortunately, due to limitations in the GUI access used to 
	load task info, this will only include tasks that are visible in the window.
	@return A list of records in the <code>TaskInfo</code> format described below
	@attributeList <code>TaskInfo</code> record
		<code>taskName</code>  The display name of the task
		<code>dueDate</code> The due date of the task or <code>missing value</code> if not set
	    <code>taskIndex</code> The one-based index of the task
*)
on getTaskInfoForFocusedList()
	
	tell application "System Events"
		tell process "Wunderlist"
			# The immediate parent element of all the task elements
			set tasksContainer to (UI element 1 of UI element 2 of UI element 3 of splitter group 1 of window "Wunderlist")
			
			# Find the N Completed Item(s) label (it is the only element with
			# exactly one button) and get its position
			set completedElement to (first UI element whose item 1 of buttons is not missing value and item 2 of buttons is missing value) of tasksContainer
			set completedPosition to position of completedElement
			set completedMinY to missing value
			
			# completedPosition will be a list of primarily missing values, with
			# one valid position. Find that position.
			repeat with theValue in completedPosition
				if class of theValue is list then
					set completedMinY to item 2 of theValue
					exit repeat
				end if
			end repeat
			
			# Get the text of each label and position of each row,
			# will include some invalid values
			set taskValues to value of static texts of UI elements of tasksContainer
			set taskPositions to position of UI elements of tasksContainer
			
			set taskInfo to {}
			set taskIndex to -1
			set taskCount to count of taskValues
			
			# Test each potential task based on its text values and position to find
			# the actual tasks
			repeat with i from 1 to (count of taskValues)
				set taskValue to item i of taskValues
				set taskPosition to item i of taskPositions
				
				# Ignore items at or below the completed label unless
				# there is no completed label on the screen
				if completedMinY is missing value or (item 2 of taskPosition) < completedMinY then
					if (count of taskValue) is 3 then
						# There are a few elements in addition to the list elements,
						# but the list elements are easily identifiable as those having 
						# 2 children.
						set {taskName, dueDate} to taskValue
						
						set taskIndex to taskIndex + 1
						
						set taskInfo to taskInfo & {{taskName:taskName, dueDate:dueDate, taskIndex:taskIndex}}
					end if
				end if
				
			end repeat
			
			taskInfo
		end tell
	end tell
	
end getTaskInfoForFocusedList

(*!
	@functiongroup Utilities
*)

(*!
	@abstract Returns the most appropriate translation of the specified string
	according to the workflow's bundle.
	@discussion This workflow uses a simple hierarchical structure for localization
	to keep the keys organized and consistent. This means that the keys are not 
	suitable for display as with simple <code>"Foo" = "Foo";</code> translation by
	word or phrase. As a result, if the key is not localized, the handler will
	return <code>missing value</code>.

	@param key the string to localize, see <code>Localizable.strings</code> within 
	this workflow for available values
	@return The localized string for the given key, or <code>missing value</code>
	if a value was not found for the key
*)
on l10n(key)
	set localized to localized string of key in bundle getWorkflowFolder()
	
	if localized = key then set localized to missing value

	return localized
end l10n

(*!
	@abstract   Returns the most appropriate translation of the specified string
	according to the localization of the Wunderlist application.
	@param key the string to localize, see <code>Localizable.strings</code> within
	the Wunderlist application bundle for available values and translations
	@return The localized string for the given key, or the key itself if no
	localization was found.
*)
on wll10n(key)
	return appl10n(key, "Wunderlist", "Localizable")
end l10n

(*!
	@abstract   Returns the most appropriate translation of the specified string
	according to the localization of the specified application.
	@param key the string to localize, see <code>Localizable.strings</code> within
	the application bundle for available values and translations
	@param appName the name of the application from which to collect a localization
	@param tableName the name of the strings file from which to load the translation
	without the extension. For example, use <code>"Localizable"</code> to reference
	<em>Example.app/Contents/Resources/en.lproj/Localizable.strings</em>
	@return The localized string for the given key, or the key itself if no
	localization was found.
*)
on appl10n(key, appName, tableName)
	tell application appName
		return localized string key from table tableName
	end tell
end l10n

(*!
	@abstract Returns the path to the workflow folder within Alfred preferences.
	@return The path to the workflow folder within Alfred preferences.
*)
on getWorkflowFolder()
	if workflowFolder is missing value then
		set workflowFolder to do shell script "pwd"
	end if

	return workflowFolder
end getWorkflowFolder

(*!
	@abstract Loads and returns qWorkflow, ensuring that it is only loaded once
	and then reused as necessary.
	@return The <code>script</code> object containing the qWorkflow library.
*)
on qWorkflow()
	if qWorkflowScript is missing value then
		set qWorkflowScript to load script POSIX file ((do shell script "pwd") & "/q_workflow.scpt")
	end if 

	return qWorkflowScript
end qWorkflow

(*!
	@abstract   Displays a notification in Notification Center.
	@discussion Loads Title, Message, and Details text from the workflow's
	localization and uses the strings to display a Notification Center
	notification to the user. Any combination of those subkeys may be 
	specified in the localization.

	@param key a <code>Messages/</code> localization key as specified in 
	<code>Localizable.strings</code>
*)
on sendNotification(key)

	set theMessage to l10n(key & "/Title")
	set theDetails to l10n(key & "/Message")
	set theExtra to l10n(key & "/Details")

	tell qWorkflow() to q_send_notification(theMessage, theDetails, theExtra)

end sendNotification

(*! 
	@functiongroup Alfred Actions
*)

(*!
	@abstract   Adds a task to Wunderlist
	@discussion To support Script Filter inputs and keyboard entry, the task may
	be prefixed by a list identifier to insert it into a specific list using
	@link addTaskToList @/link. The prefix ensures that the task is added to a
	specific list. Without it, for example if <code>task</code> is simply
	<code>2% milk</code> the task will be added to whichever list is currently
	visible. 

	If Wunderlist is on a screen that does not allow task input, such as search
	results or the <em>Assigned to Me</em> screen, the task will be added in the
	Inbox.

	After calling this handler, the previous application is reactivated. However, if 
	<code>task</code> is not specified, Wunderlist will remain active with the 
	keyboard focus on the task input for the specified list.
	@attributeblock List Identifiers
	To identify a list by name, <code>task</code> should contain the list name
	and the text of the task separated by a colon. 
	<pre><code>    Grocery List:2% milk</code></pre>

	To identify a list by index, <code>task</code> should contain the list index
	and the text of the task separated by two colons. This is primarily for 
	internal use.
	<pre><code>    4::2% milk</code></pre>
	@param task The text of the task, optionally prefixed with a numeric or textual
	list identifier.
*)
on addTask(task)

	if task is not "" then
		# The format used to add a task to a specific list, e.g. 5::2% milk
		set components to qWorkflow()'s q_split(task, "::")

		# If a list index is specified, add the task to it
		if count of components is 2 then
			set {listIndex, task} to components

			addTaskToList(listIndex as integer, task)
			return
		end if

		set components to qWorkflow()'s q_split(task, ":")

		# If a list name is specified, add the task to that list
		if count of components is 2 then
			set {listName, task} to components

			set listIndex to getIndexOfListNamed(listName)

			if listIndex > 0 then
				addTaskToList(listIndex as integer, task)
				return
			end if
		end if

		launchWunderlistIfNecessary()
		
		activateWunderlist()
		
		focusTaskInput()
		
		tell application "System Events"

			# Populate the field with the text of the task
			keystroke task
			
			# Return key to add the task
			keystroke return
			
		end tell

		# Show that the task was added
		delay 1
		
		activatePreviousApplication()

	else 

		launchWunderlistIfNecessary()
		
		# If there is no task, just show the Wunderlist window and prepare
		# for task entry.
		activateWunderlist()
		
		focusTaskInput()

	end if
	
end addTask

(*!
	@abstract   Adds a task to the specified list in Wunderlist
	@discussion Uses @link focusListAtIndex @/link to focus the specified list,
	then inserts the task.

	If the specified list does not allow task input, such as <em>Assigned to Me</em>
	or <em>Week</em>, the task will be added in the Inbox.

	After calling this handler, the previous application is reactivated. However, if 
	<code>task</code> is not specified, Wunderlist will remain active with the 
	keyboard focus on the task input for the specified list.

	@param listIndex The integer one-based index of the list as it appears in the 
	list table
	@param task The text of the task
*)
on addTaskToList(listIndex, task)

	launchWunderlistIfNecessary()
	
	activateWunderlist()

	if listIndex >= 0 then
		focusListAtIndex(listIndex)
	end if
	
	focusTaskInput()
	
	# If a task is specified, add it then return to the previous application
	if task is not "" then
		tell application "System Events"

			# Populate the field with the text of the task
			keystroke task
			
			# Return key to add the task
			keystroke return
			
		end tell

		# Show that the task was added
		delay 1
		
		activatePreviousApplication()
	end if
	
end addTask

(*!
	@abstract   Adds a task to the Inbox list in Wunderlist
	@discussion Provides a shortcut for entering tasks directly in the Inbox.

	After calling this handler, the previous application is reactivated. However, if 
	<code>task</code> is not specified, Wunderlist will remain active with the 
	keyboard focus on the task input for the Inbox.

	@param task The text of the task
*)
on addTaskToInbox(task)

	launchWunderlistIfNecessary()
	
	activateWunderlist()
	
	focusInbox()
	
	focusTaskInput()
	
	# If a task is specified, add it then return to the previous application
	if task is not "" then
		
		tell application "System Events"

			# Populate the task input field with the text of the task
			keystroke task
			
			# Return key to add the task
			keystroke return
			
		end tell
		
		# Since we can't do this entire process in the background, at least
		# allow the user a moment to see what happened.
		delay 1.5
		
		# Return the user to whichever list was previously visible
		focusPreviousList()
		
		activatePreviousApplication()
		
	end if
	
end addTaskToInbox

(*!
	@abstract   Adds a new list to Wunderlist
	@discussion After calling this handler, Wunderlist remains activated with the keyboard focus 
	on the task input for the new list.

	@param listName The name of the new list
*)
on addList(listName)

	launchWunderlistIfNecessary()
	
	activateWunderlist()
	
	# Show the lists pane
	setWindowViewNormal()
	
	# Always the top item in the task list
	focusInbox()
	
	tell application "System Events"
		
		# Use Command-L to create a new list
		keystroke "l" using command down
		
		# There is some delay before the new list is added
		delay 0.75
		
		# Use Up arrow to focus on the new list at the bottom
		key code 126
		
		# Use Option-R to rename the new list
		keystroke "r" using option down

		# Insert the name of the list
		keystroke listName
		
		# Return key to rename the list
		keystroke return
		
	end tell

	focusTaskInput()
	
end addList

(*!
	@abstract   A Script Filter input that shows the user's lists in Alfred, allowing
	a task to be added to a specific list.
	@discussion Queries the Wunderlist UI to provide all of the lists into which
	new tasks can be added. The response is formatted for Alfred to display in
	a way that allows the user to type their task, then action a specific list to
	insert the task there.

	After selecting one of these options, the final query will be a concatenation 
	of the list index and the user's task in a format suitable for 
	@link addTaskToList @/link:
	<pre><code>    5::2% milk</code></pre>
	@param task The text of the task
*)
on showListOptions(task)

	launchWunderlistIfNecessary()

	# Load qWorkflow to format the output
	set wf to qWorkflow()'s new_workflow()

	set taskComponents to qWorkflow()'s q_split(task, ":")
	set listFilter to item 1 of taskComponents
	set task to ""

	if count of taskComponents is 2 then
		set task to item 2 of taskComponents
	end if

	set allLists to getListInfoInWorkflow(wf)
	set writableLists to {}
	set matchingLists to {}
	set canAutocomplete to true

	# These lists do not allow addition of new tasks
	set readonlyLists to {wll10n("smart_list_all"), wll10n("smart_list_assigned_to_me"), wll10n("smart_list_completed"), wll10n("smart_list_week")}

	# Skip "smart lists" that do not allow creation of new tasks
	repeat with listInfo in allLists
		if listInfo's listName is not in readonlyLists then set writableLists's end to listInfo
	end repeat

	# Find lists matching the user's filter
	repeat with listInfo in writableLists
		ignoring case and diacriticals
			if listInfo's listName contains listFilter then set matchingLists's end to listInfo
		end ignoring
	end repeat

	# There are no matching lists, so just let the user type a
	# task and select a list later using the arrow keys
	if count of matchingLists is 0 then
		set canAutocomplete to false
		set matchingLists to writableLists

		# If the user did not type a colon the listFilter will
		# contain the text of the task. We know it doesn't match
		# any of the lists so now we can just reassign this.
		if task is "" then
			set task to listFilter
		end if
	# Show "a task" as a placeholder in "Add [a task] to this list"
	else if task is "" then
		set task to "a task"
	end if

	# TODO: filter and/or sort lists by user input
	repeat with listInfo in matchingLists
		set listName to listName of listInfo

		set taskCount to taskCount of listInfo
		set listIndex to listIndex of listInfo
		# TODO: option to sort lists by most frequently used in Alfred
		# temporarily disabled by not providing a uid
		set theUid to missing value # "com.ipaterson.alfred.wunderlist.lists." & listName
		set theAutocomplete to missing value
		set theArg to listIndex as text & "::" & task
		set theSubtitle to "Add " & task & " to this list"
		set theIcon to "/generic.png"
		set isValid to true 

		# If autocompletion is possible, set isValid to false
		# to enable autocomplete on tab
		if canAutocomplete then
			set theAutocomplete to listName & ":"
			set isValid to false
		end if

		# TODO: find a way to determine whether the task count is
		# accurate. Currently the Wunderlist UI populates the label
		# with a random value if there are no tasks in a list.
		# Unfortunately it does not seem possible to distinguish
		# whether the number is visible or not based on the attributes
		# available to AppleScript.
		(*
		set theSubtitle to taskCount as text

		if taskCount is 1 then
			set theSubtitle to theSubtitle & " task"
		else
			set theSubtitle to theSubtitle & " tasks"
		end if
		*)

		# Choose the proper icon for each list
		if listName is wll10n("smart_list_inbox") then
			set theIcon to "/inbox.png"
		else if listName is wll10n("smart_list_today") then
			set theIcon to "/today.png"
		else if listName is wll10n("smart_list_starred") then
			set theIcon to "/starred.png"
		end if

		# Load the icon based on the configured theme 
		set theIcon to "lists/" & iconTheme & theIcon
		
		add_result of wf given theUid:theUid, theArg:theArg, theTitle:listName, theSubtitle:theSubtitle, theAutocomplete:theAutocomplete, isValid:isValid, theIcon:theIcon, theType:missing value
	end repeat
	
	return wf's to_xml("")
	
end showListOptions
