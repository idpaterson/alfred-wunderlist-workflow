(*!
	@header     UI Interaction with Lists
	@abstract   Interacts with the Wunderlist UI for reading and modifying lists.
	@discussion 
	@version    0.2
*)

(*! 
	@abstract Designates that items in the list should be sorted alphabetically by name.
*)
property sortTypeAlphabetical : 3

(*! 
	@abstract Designates that items in the list should be sorted chronologically by due date.
*)
property sortTypeDueDate : 2

(*! 
	@abstract Designates that items in the list should be sorted alphabetically by assignee.
*)
property sortTypeAssignee : 1

# Toolbar Constants
# 
# The toolbar on Wunderlist is not available by UI traversal, leaving no way for 
# AppleScript to navigate or inspect it. All of the values below are subject to
# change in future versions of Wunderlist.

# The button in the floating lists toolbar that allows people to be invited to a list
property inviteToolbarButtonIndex : 1

# The button in the floating lists toolbar that allows the tasks in a list to be emailed
property emailToolbarButtonIndex : 2

# The button in the floating lists toolbar that allows the tasks in a list to be printed
property printToolbarButtonIndex : 3

# The button in the floating lists toolbar that allows the tasks in a list to be sorted
property sortToolbarButtonIndex : 4

# The height of buttons that appear over the toolbar
property toolbarMenuButtonHeight : 35

# The number of buttons in the toolbar
property toolbarButtonCount : 4

(*! 
	@functiongroup Navigating Wunderlist
*)

(*!
	@abstract   Moves focus within the app to the specified list.
	@discussion A mouse click is used to quickly navigate to the desired list.

	@param listIndex The numerical one-based index of the desired list.
*)
on focusListAtIndex(listIndex)

	set listInfo to item listIndex of getListInfo()

	clickAt(listInfo's listPosition)

	delay 0.2
	
end focusListAtIndex


(*!
	@abstract   Reorders the current list based on the specified sort type.
	@discussion Some lists do not support all sort types. In general, the following
	should hold true:
	<dl>
	<dt>Sort Alphabetically</dt>
	<dd>Supported in any list, except Today and Week, that has two or more tasks.</dd>
	<dt>Sort by Due Date</dt>
	<dd>Supported in any list, except Today and Week, that has two or more tasks at 
	least one of which having a due date.</dd>
	<dt>Sort by Assignee</dt>
	<dd>Supported in any list, except Today and Week, that has two or more tasks at
	least one of which having an assignee.</dd>
	</dl>

	The only way to sort lists in Wunderlist is by using the pointer to
	click the toolbar that floats at the bottom of the task list. Therefore, this 
	feature is very dependent on the calculations used to determine the position
	of the sorting buttons.

	@param sortType any of the predefined sort type globals.
*)
on sortCurrentList(sortType)

	set tasksContainer to getTasksContainerElement()
	set sortButtonCenter to getCenterOfTasksContainerToolbarButton(sortToolbarButtonIndex)

	delay 0.1

	clickAt(sortButtonCenter)

	delay 0.5

	# The sortType is reverse indexed based on the menu order so that the height 
	# of the toolbar menu button can be subtracted the number of times specified
	# by the sortType in order to click the button for that type.
	set {xPos, yPos} to sortButtonCenter
	set yPos to yPos - sortType * toolbarMenuButtonHeight

	clickAt({xPos, yPos})

end sortCurrentList


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
	@abstract Ensures that the next time the list info is requested, it will be
	reloaded from the UI rather than the cache.
*)
on invalidateListInfoCache()
	set wf to getCurrentWorkflow()

	wf's set_value("listsUpdatedDate", date ("1/1/2000" as string) , "")
end invalidateListInfoCache


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
	@functiongroup Finding Wunderlist UI Elements
*)

(*!
	@abstract Returns the <code>UI element</code> that holds everything in the lists 
	panel, or <code>missing value</code> if the lists panel is not visible, such as in 
	collapsed or minified view.
*)
on getListsContainerElement()

	tell application "System Events"
		tell process "Wunderlist"

			if (count of UI elements of splitter group 1 of window "Wunderlist") is 2 then
				return UI element 1 of splitter group 1 of window "Wunderlist"
			else
				return missing value
			end if
			
		end tell
	end tell

end getListsContainerElement


(*!
	@functiongroup Interacting with Wunderlist
*)

(*!
	@abstract Creates a new list with the specified name.

	@param listName The name of the list
*)
on addNewList(listName)

	activateWunderlist()

	clickMenuItem("File", "Add New List")

	# There is some delay before the new list is added
	delay 0.75

	# Insert the name of the list
	insertText(listName)
	
	# Return key to rename the list
	tell application "System Events" to keystroke return

end addNewList
