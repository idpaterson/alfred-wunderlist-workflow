set testId to "2.2.0"
set command to "wlin"
set precondition to "Wunderlist should be running on the current desktop"
set postcondition to "The Inbox is selected in Wunderlist and no task has been added"

display dialog precondition buttons {"Go", "Cancel"} default button 1 cancel button 2 with title "Test " & testId & " Preconditions"

tell application "Alfred 2" to search command

delay 2

tell application "System Events" 
	tell process "Alfred 2" to keystroke return

	delay 3

	set result to button returned of (display dialog postcondition buttons {"Pass", "Fail"} default button 1 with title "Please verify")
	if result is "Pass"
		1
	else
		0
	end if

end tell
