delay 3

tell application "Wunderlist" to activate

tell application "System Events" 
	tell process "Wunderlist" 
		keystroke "f" using command down

		keystroke "#workflowtest"
	end tell
end tell
