set testId to "3.2.1"
set listName to "Sample list " & testId
set command to "wllist " & listName
set precondition to "Press Cmd+W in Wunderlist to close the main window, then activate a different app on the same desktop before pressing Go. Wunderlist should be running on the same desktop but with no visible windows."
set postcondition to "New list " & listName & " added to Wunderlist"

display dialog precondition buttons {"Go", "Cancel"} default button 1 cancel button 2 with title "Test " & testId & " Preconditions"

tell application "Alfred 2" to search command

delay 2

tell application "System Events" 
	tell process "Alfred 2" to keystroke return

	delay 4

	set result to button returned of (display dialog postcondition buttons {"Pass", "Fail"} default button 1 with title "Please verify")
	if result is "Pass"
		1
	else
		0
	end if

end tell
