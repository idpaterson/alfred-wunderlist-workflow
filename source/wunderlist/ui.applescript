(*!
	@header     UI Interaction
	@abstract   Interacts with the Wunderlist UI for reading and modifying data.
	@discussion 
*)

(*! 
	@functiongroup Application Interactions
*)

# Keep track of the current app
property originalApp : missing value

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
	@functiongroup Navigating Wunderlist
*)

(*!
	@abstract   Moves focus within the app to the Inbox list.
	@discussion Uses the keyboard to move focus within the app to the Inbox list. 
	The Inbox list is a good reference point because it is always at the top of the 
	lists table.

	The procedure for accessing the Inbox from any point in the app is as follows:
	1. <code>&#x2318;+f</code> Begin a search
	2. Perform a search that will probably not return results and will not be too 
	distracting. 3 space characters works fine.
	3. <code>&#x2318;+n</code> Navigate to the Inbox, focused on the Inbox list
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
	1. <code>&#x2318;+f</code> Return to the search input
	2. Press the delete key to clear the search, Wunderlist will switch back to the previously viewed list
	3. <code>&#x2318;+n</code> Move focus out of the search box into the task list
	4. <code>&#x21E7;+tab</code> Return focus to the list table
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
	1. <code>&#x2318;+n</code> Focus the task input, or in some cases focus the Inbox
	2. <code>&#x2318;+n</code> For good measure in case the previous command focused the Inbox
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
	@functiongroup Accessing Data in Wunderlist
*)

(*!
	@abstract Loads some basic information about all of the visible lists in Wunderlist.
	@discussion Wunderlist exposes a small amount of information about the lists that
	can be retrieved by traversing the UI. This information includes the name of each
	list and its number of tasks.

	Unfortunately, the number of tasks returned is undefined when there are no tasks in 
	a list. Wunderlist does not set the value of the task count label to zero, nor does
	it hide the label in a way that is detectable by AppleScript. The value in the label
	appears to change in an undefined way, so unfortunately at this time the task
	count is unreliable.

	The list info is cached as specified by @link listCacheInSeconds @/link
	to optimize repetitive access of the list, as with an Alfred Script Filter.

	The keys <code>lists</code> and <code>listsUpdatedDate</code> in the default
	<code>settings.plist</code> are used to track the lists state.

	@return A list of records in the <code>ListInfo</code> format described below
	@attributeList <code>ListInfo</code> record
		<code>listName</code>  The display name of the list
		<code>taskCount</code> The number of uncompleted tasks in the list
	    <code>listIndex</code> The one-based index of the list
*)
on getListInfo()

	set wf to getCurrentWorkflow()

	# Load the list info and the cache date
	set listInfo to wf's get_value("lists", "")
	set lastUpdatedDate to wf's get_value("listsUpdatedDate", "")

	# Reload the list info if the cached data is missing or expired
	if lastUpdatedDate is not missing value and current date - lastUpdatedDate ² listCacheInSeconds then
		return listInfo
	end if

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
			
		end tell
	end tell

	wf's set_value("lists", listInfo, "")
	wf's set_value("listsUpdatedDate", current date, "")

	return listInfo
	
end getListInfo

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
