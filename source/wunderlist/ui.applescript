(*!
	@header     UI Interaction
	@abstract   Interacts with the Wunderlist UI for reading and modifying data.
	@discussion 
	@version    0.2
*)

(*! 
	@functiongroup Application Interactions
*)

# Keep track of the current app
property originalApp : missing value

# Keep track of the currently selected list
property originalListInfo : missing value

(*! 
	@abstract Causes Wunderlist to become the active application.
*)
on activateWunderlist()

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
	@deprecated in version 0.2
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
	
	# Ensure we can return to the current active application later
	set originalApp to path to frontmost application as text
	
	# Wunderlist has to be running, if not we need to launch it and wait
	if application appName is not running then
		tell application appName to launch
		
		# Wait for application to launch
		tell application "System Events"
			# Wait up to ~3 seconds, if any longer than that Wunderlist may
			# be assigned to a specific desktop other than the current one.
			set attempts to 0
			repeat until count of windows of process appName > 0 or attempts > 60
				set attempts to attempts + 1
				delay 0.05
			end repeat
		end tell
	end if

	try 
		tell application "System Events" 
			set mainWindow to window appName of process appName

			# If the window is minimized, give it time to reappear
			if miniaturized of mainWindow is true then
				set miniaturized of mainWindow to false
				delay 1
			end if
		end tell
	on error
		# Wunderlist may not be on the current desktop, so switch to it.
		tell application appName to activate

		# Wunderlist may not be launching; if the user closed the window, such
		# as with Cmd+W, or minimized the window, use the new task command to 
		# bring the window back.
		focusTaskInput()

		# Wait for the window to become available
		tell application "System Events"
			repeat until count of windows of process appName > 0
				delay 0.05
			end repeat

			# The window is programmatically available, let's make sure it is
			# also initialized and ready for input
			delay 0.25
		end tell
	end try

end launchWunderlistIfNecessary

(*! 
	@functiongroup Navigating Wunderlist
*)

(*!
	@abstract Performs a mouse click at the specified position on the screen,
	then resets the mouse to its original position.

	@param aPoint The {x,y} coordinate point to click, relative to the screen
*)
on clickAt(aPoint)

	set x to (item 1 of aPoint)
	set y to (item 2 of aPoint)

	do shell script "bin/cliclick -r c:" & x & "," & y & " p"
	
end clickAt


(*!
	@abstract   Moves focus within the app to the specified list.
	@discussion A mouse click is used to quickly navigate to the desired list.

	@param listIndex The numerical one-based index of the desired list.
*)
on focusListAtIndex(listIndex)

	set listInfo to item listIndex of getListInfo()

	clickAt(listInfo's listPosition)
	
end focusListAtIndex


(*!
	@abstract   Returns focus to the last list viewed prior to navigating lists.
	@discussion @link recordPreviousList @/link must be called prior to navigating
	lists, otherwise it will not be possible to return to the previous list.

	@see focusListAtIndex
*)
on focusPreviousList()
	
	if originalListInfo is not missing value then
		clickAt(originalListInfo's listPosition)
	end if
	
end focusPreviousList


(*!
	@abstract   Records the ListInfo for the currently selected list so that it
	can be reselected later.
	@discussion This must be called before switching to a different list in order
	to make use of @link focusPreviousList @/link. 

	@see getListInfoForActiveList
*)
on recordPreviousList()

	if originalListInfo is missing value then
		set originalListInfo to getListInfoForActiveList()
	end if

end recordPreviousList


(*!
	@abstract   Switches keyboard focus to the task input field.
	@discussion In certain views it is necessary to use the New Task shortcut twice
	because the first time switches the UI to the Inbox list.

	The procedure for returning to the previous list is as follows:
	1. <code>&#x2318;+n</code> Focus the task input, or in some cases focus the Inbox
	2. <code>&#x2318;+n</code> For good measure in case the previous command focused the Inbox
*)
on focusTaskInput()
	
	tell application "System Events"
		
		# Focus task input to create a new task
		# If searching, Command-N is required twice to create a task
		keystroke "n" using command down
		delay 0.05
		keystroke "n" using command down
		delay 0.05
		
	end tell
	
end focusTaskInput

(*!
	@abstract Emulates a click on the star button in the task input field, toggling its
	value between starred and not starred.
	@discussion The star button only appears after the task input has been focused. In order
	to have any effect, this must be called after the task input is focused and before the
	task is entered.
*)
on toggleStarInTaskInput()

	set listsPanel to getListsPanelElement()
	set starButton to getStarButtonInTaskInputElement()

	tell application "System Events"
		tell process "Wunderlist"
	
			set starPosition to my positionWithinTasksPanelAdjustedForListsPanel(position of starButton)

			# Clicking at the position does not work, offset by 10px in each direction
			set item 1 of starPosition to (item 1 of starPosition) + 10
			set item 2 of starPosition to (item 2 of starPosition) + 10

		end tell
	end tell

	clickAt(starPosition)

end toggleStarInTaskInput

(*!
	@abstract   Sends the specified text to the first receiver of the frontmost application.
	@discussion Text is sent to the application via the clipboard, ensuring that any special
	characters are retained.

	@param theText The text to insert
*)
on insertText(theText)
	
	set originalContents to the clipboard
	set the clipboard to theText as text

	# Cmd+V to paste
	tell application "System Events" to keystroke "v" using command down
	delay 0.25

	set the clipboard to originalContents

end insertText

(*!
	@abstract Switches to the "Normal" view in Wunderlist where both the list and 
	tasks are visible.
*)
on setWindowViewNormal()
		
	# Make sure Wunderlist is in Normal View
	tell application "System Events" to keystroke "1" using command down
	delay 0.05
	
end setWindowViewNormal

(*!
	@functiongroup Finding Wunderlist UI Elements
*)

(*!
	@abstract Returns the <code>UI element</code> containing the tasks and other 
	associated elements in the current list.
*)
on getTasksContainerElement()

	tell application "System Events"
		tell process "Wunderlist"

			return UI element 1 of UI element 2 of last UI element of splitter group 1 of window "Wunderlist"
			
		end tell
	end tell

end getTasksContainerElement

(*!
	@abstract   Returns the <code>UI element</code> representing the task input field.
*)
on getTaskInputElement()

	set tasksContainer to getTasksContainerElement()

	tell application "System Events"
		tell process "Wunderlist"

			return first UI element of tasksContainer whose position of item 3 of buttons is not missing value
			
		end tell
	end tell

end getTaskInputElement

(*!
	@abstract   Returns the star <code>button</code> in the task input field.
	@discussion The element will be returned regardless of whether it is currently visible
	or not. It is necessary to focus the task input to ensure that the star button is
	visible and clickable.
*)
on getStarButtonInTaskInputElement()

	set taskInput to getTaskInputElement()

	tell application "System Events"
		tell process "Wunderlist"

			return item 3 of buttons of taskInput
			
		end tell
	end tell

end getStarButtonInTaskInputElement

(*!
	@abstract Returns the <code>UI element</code> that holds everything in the lists 
	panel, or <code>missing value</code> if the lists panel is not visible, such as in 
	collapsed or minified view.
*)
on getListsPanelElement()

	tell application "System Events"
		tell process "Wunderlist"

			if (count of UI elements of splitter group 1 of window "Wunderlist") is 2 then
				return UI element 1 of splitter group 1 of window "Wunderlist"
			else
				return missing value
			end if
			
		end tell
	end tell

end getListsPanelElement

(*!
	@abstract Adjusts the specified position of any element in the tasks panel
	as necessary if the lists panel is visible.
	@discussion The position of any UI element within the tasks panel is incorrect if
	the lists panel is visible; both lists report their position as if they are aligned
	to the upper left corner of the Wunderlist window. If the lists panel is visible,
	the returned position will be offset on the x coordinate by the width of the panel.
*)
on positionWithinTasksPanelAdjustedForListsPanel(thePosition)

	set listsPanel to getListsPanelElement()

	if listsPanel is not missing value then
		tell application "System Events"
			tell process "Wunderlist"
				set {listsPanelWidth} to size of listsPanel
				set item 1 of thePosition to (item 1 of thePosition) + listsPanelWidth
			end tell
		end tell
	end if

	return thePosition

end positionWithinTasksPanelAdjustedForListsPanel

(*! 
	@functiongroup Accessing Data in Wunderlist
*)

(*!
	@abstract Loads some basic information about all of the visible lists in Wunderlist.
	@discussion Wunderlist exposes a small amount of information about the lists that
	can be retrieved by traversing the UI. This information includes the name of each
	list, its number of tasks.

	Unfortunately, the number of tasks returned is undefined when there are no tasks in 
	a list. Wunderlist does not set the value of the task count label to zero, nor does
	it hide the label in a way that is detectable by AppleScript. The value in the label
	appears to change in an undefined way, so unfortunately at this time the task
	count is unreliable.

	The list info is cached as specified by @link listCacheInSeconds @/link
	to optimize repetitive access of the list, as with an Alfred Script Filter.

	The keys <code>lists</code> and <code>listsUpdatedDate</code> in the default
	<code>settings.plist</code> are used to track the lists state.

	@return A list of records in the <code>ListInfo</code> format described below,
	sorted in the order displayed in Wunderlist.
	@attributeList <code>ListInfo</code> record
		<code>listName</code>  The display name of the list
		<code>taskCount</code> The number of uncompleted tasks in the list
	    <code>listIndex</code> The one-based index of the list in the UI
	    <code>listPosition</code> The position of the list in the UI in {x, y} format
*)
on getListInfo()

	set wf to getCurrentWorkflow()

	# Load the list info and the cache date
	set listInfo to wf's get_value("lists", "")
	set lastUpdatedDate to wf's get_value("listsUpdatedDate", "")

	# Reload the list info if the cached data is missing or expired
	if lastUpdatedDate is not missing value and listInfo is not missing value and current date - lastUpdatedDate ² listCacheInSeconds then
		if (class of listInfo) is record then
			return listInfo's theList
		else
			return listInfo
		end if
	end if

	set listInfo to {}

	tell application "System Events"
		tell process "Wunderlist"
			if count of windows > 0 then
				# The immediate parent element of all the list elements
				set listsContainer to UI element 1 of UI element 1 of UI element 1 of UI element 1 of splitter group 1 of window "Wunderlist"
				
				set {listValues, listPositions} to {value, position} of static texts of UI elements of listsContainer

				repeat with i from 1 to count of listValues
					set listValue to item i of listValues

					if (count of listValue) is 2 then
						# There are a few elements in addition to the list elements,
						# but the list elements are easily identifiable as those having 
						# 2 children.
						set {listName, taskCount} to listValue

						# Get the position of the first static text
						set listPosition to item 1 of item i of listPositions
						
						set taskCount to taskCount as integer
						
						set listInfo to listInfo & {{listName:listName, taskCount:taskCount, listIndex:-1, listPosition:listPosition}}
					end if
				end repeat
			end if
		end tell
	end tell

	script sorter
		on getYPositionOfListInfo(listInfo)
			# Grab the Y component of the position
			return item 2 of listInfo's listPosition
		end getYPositionOfListInfo
	end script

	# Sort the list based on the actual y-axis order of the list. When the
	# list is scrolled, cells are reused which places them at the end of the
	# UI elements list. This ensures that we show the results in the order
	# in which the user will see them in Wunderlist.
	set listInfo to quickSortWithKeyHandler(listInfo, sorter's getYPositionOfListInfo)

	# Set the list index based on the order of the sorted list
	repeat with i from 1 to count of listInfo
		set listIndex of item i of listInfo to i
	end repeat

	# Allow the previous value to persist even if it is expired in the case
	# where we cannot load newer list data.
	if count of listInfo > 0 then
		# In Mavericks, a property list becomes immediately corrupted when a 
		# list value is added to it. The property list is zeroed out and 
		# becomes immediately unusable. To work around that we have to use
		# a record instead of a list.
		wf's set_value("lists", {theList: listInfo}, "")
		wf's set_value("listsUpdatedDate", current date, "")
	end if

	return listInfo
	
end getListInfo

(*!
	@abstract Loads information about the currently selected list in Wunderlist.
	@discussion The active list is highlighted in the Wunderlist UI, but finding
	it with UI traversal is not straightforward. In order to find which list is
	selected, the <em>Rename Selected List</em> menu option is required. It 
	creates an editable text element that is easy to isolate with AppleScript.

	From the text element the name of the list can be retrieved. This allows the
	proper result from @link getListInfo @/link to be returned.

	@see getListInfo
	@return A records in the <code>ListInfo</code> format
*)
on getListInfoForActiveList()

	tell application "System Events"
		tell process "Wunderlist"
			# Switch to Collapsed View 
			click menu item 9 of menu 1 of menu bar item 6 of menu bar 1

			# Get the list name from the window title label
			set theListName to value of static text 1 of window "Wunderlist" 

			# Return to Normal View
			click menu item 8 of menu 1 of menu bar item 6 of menu bar 1

		end tell
	end tell

	set listsInfo to getListInfo()

	# Return the matching list
	repeat with listInfo in listsInfo
		if listName of listInfo is theListName
			return listInfo
		end 
	end repeat

end getListInfoForActiveList

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
			set completedElement to (first UI element whose position of item 1 of buttons is not missing value and position of item 2 of buttons is missing value) of tasksContainer
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
	@abstract Ensures that the next time the list info is requested, it will be
	reloaded from the UI rather than the cache.
*)
on invalidateListInfoCache()
	set wf to getCurrentWorkflow()

	wf's set_value("listsUpdatedDate", date ("1/1/2000" as string) , "")
end invalidateListInfoCache
