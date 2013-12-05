(*!
	@header     UI Interaction
	@abstract   Interacts with the Wunderlist UI for reading and modifying data.
	@discussion 
	@version    0.2
*)

# Keep track of the current app
property originalApp : missing value

(*! 
	@functiongroup Application Interactions
*)

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
	@functiongroup UI Interaction
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
	@functiongroup Wunderlist Layout Commands
*)

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
	@abstract Switches to the "Collapsed" view in Wunderlist where only the tasks 
	are visible and the name of the current list is shown in the title bar.
*)
on setWindowViewCollapsed()
		
	# Make sure Wunderlist is in Collapsed View
	tell application "System Events" to keystroke "2" using command down
	delay 0.05
	
end setWindowViewCollapsed


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
	@abstract Adjusts the specified position of any element in the tasks panel
	as necessary if the lists panel is visible.
	@discussion The position of any UI element within the tasks panel is incorrect if
	the lists panel is visible; both lists report their position as if they are aligned
	to the upper left corner of the Wunderlist window. If the lists panel is visible,
	the returned position will be offset on the x coordinate by the width of the panel.
*)
on positionWithinTasksPanelAdjustedForListsPanel(thePosition)

	set listsPanel to getListsContainerElement()

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
