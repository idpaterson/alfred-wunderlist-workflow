delay 3

tell application "Wunderlist" to activate

tell application "System Events" 
	tell process "Wunderlist" 
		keystroke "f" using command down

		delay 0.5

		keystroke "#workflowtest"
	end tell
end tell
