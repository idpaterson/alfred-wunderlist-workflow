(*!
	@header     UI Interaction with Tasks
	@abstract   Interacts with the Wunderlist UI for reading and modifying tasks.
	@discussion 
	@version    0.2
*)

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

	set listsPanel to getListsContainerElement()
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
	@functiongroup Accessing Data in Wunderlist
*)

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
	@functiongroup Finding Wunderlist UI Elements
*)

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
