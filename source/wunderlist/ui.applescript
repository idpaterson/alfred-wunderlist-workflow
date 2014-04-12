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

# Keep track of the original clipboard
property originalClipboard : missing value

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

			# If the window is minimized, give it time to reappear.
			# The subrole of the Wunderlist window changes from "AXStandardWindow" 
			# to "AXDialog" when it is minimized. The miniaturized property does 
			# not work.
			if subrole of mainWindow is "AXDialog" then
				clickMenuItem("Window", "Wunderlist")
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
	@abstract Determines whether the user has enabled accessibility control for
	Alfred, a necessary step to allow the workflow to function properly, and
	prompts them to update the setting if necessary.
	@discussion The accessibility control setting allows this and other Alfred
	workflows to access the UI of running applications. This is necessary for 
	access to and interaction with the Wunderlist UI.

	The instructions for enabling this setting vary depending on the current
	operating system version. In OS X Mavericks the setting is specific to each
	app, while previously it was controlled by a global checkbox.
	@throws The error <em>UI control is not enabled</em> is thrown if the user 
	must update the accessibility setting. In most cases you should not catch 
	the error; the workflow should abort if it does not have access to Wunderlist.
*)
on requireAccessibilityControl()

	tell application "System Events" to set controlEnabled to UI elements enabled

	if not controlEnabled then
		set osVersion to system version of (system info)

		# Compare version numbers such that 1.10 > 1.9
		considering numeric strings
			# Show the Privacy pane on Mavericks
			if osVersion >= "10.9" then
				sendNotification("Messages/Accessibility is disabled (per-app privacy setting)")

				tell application "System Preferences"
					set securityPane to pane id "com.apple.preference.security"
					tell securityPane to reveal anchor "Privacy_Accessibility"
				activate
				end tell

			# Show the Accessibility pane on earlier OS X
			else
				sendNotification("Messages/Accessibility is disabled (global checkbox)")

				tell application "System Preferences"
					set current pane to pane id "com.apple.preference.universalaccess"
					activate
				end tell
			end if
		end considering

		error "UI control is not enabled"
	end if

end requireAccessibilityControl


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
	
	if originalClipboard is missing value then
		set originalClipboard to the clipboard

		# Make sure that the text used internally is not added as the original clipboard
		# contents on future invocations of insertText
		if originalClipboard is missing value then
			set originalClipboard to ""
		end if
	end if

	set the clipboard to theText as text

	# Cmd+V to paste
	clickMenuItem("Edit", "Paste")
	delay 0.2

end insertText


(*!
	@abstract   Clicks the specified item in the specified menu.
	@discussion The menu items should be specified in English. The items will be localized to 
	ensure compatibility with Wunderlist installs in other locales.

	@param theMenu The name of the menu (e.g. File, Edit)
	@param theMenuItem The name of the menu item (e.g. Copy, Page Setup...)
*)
on clickMenuItem(theMenu, theMenuItem)

	set theMenu to wll10n(theMenu)
	set theMenuItem to wll10n(theMenuItem)

	tell application "System Events" 
		tell process "Wunderlist"

			click menu item theMenuItem Â
			of menu 1 of menu bar item theMenu of menu bar 1
			
		end tell
	end tell

end clickMenuItem


(*!
	@abstract   Determines whether the specified menu item is currently enabled.
	@discussion The menu items should be specified in English. The items will be localized to 
	ensure compatibility with Wunderlist installs in other locales.

	@param theMenu The name of the menu (e.g. File, Edit)
	@param theMenuItem The name of the menu item (e.g. Copy, Page Setup...)

	@return A boolean indicating whether the specified menu item is enabled.
*)
on isMenuItemEnabled(theMenu, theMenuItem)

	set theMenu to wll10n(theMenu)
	set theMenuItem to wll10n(theMenuItem)

	tell application "System Events" 
		tell process "Wunderlist"

			return enabled of menu item theMenuItem Â
			of menu 1 of menu bar item theMenu of menu bar 1
			
		end tell
	end tell

end isMenuItemEnabled


(*!
	@abstract   Presses the X button to clear any search field text.
	@discussion If there is no text in the search field this will return immediately;
	otherwise there is a short delay to allow time for the UI to reset from the search.
*)
on clearSearchField()

	tell application "System Events" 
		tell process "Wunderlist"

			set searchButtons to buttons of text field 1 of window "Wunderlist"

			if count of searchButtons = 2 then
				# The X button that clears results
				click item 2 of searchButtons
				delay 1
			end if
			
		end tell
	end tell

end clearSearchField

(*!
	@functiongroup Wunderlist Layout Commands
*)

(*!
	@abstract Switches to the "Normal" view in Wunderlist where both the list and 
	tasks are visible.
*)
on setWindowViewNormal()
		
	# Make sure Wunderlist is in Normal View
	clickMenuItem("Window", "Normal View")
	delay 0.05
	
end setWindowViewNormal


(*!
	@abstract Switches to the "Collapsed" view in Wunderlist where only the tasks 
	are visible and the name of the current list is shown in the title bar.
*)
on setWindowViewCollapsed()
		
	# Make sure Wunderlist is in Collapsed View
	clickMenuItem("Window", "Collapsed View")
	delay 0.05
	
end setWindowViewCollapsed
