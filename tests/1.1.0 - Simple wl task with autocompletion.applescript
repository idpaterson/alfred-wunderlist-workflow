set testId to "1.1.0"
set task to "Sample task #workflowtest " & testId
set command to "wl to"
set precondition to "Wunderlist should be running on the current desktop"
set postcondition to "New task " & task & " added in the Today list"

display dialog precondition buttons {"Go", "Cancel"} default button 1 cancel button 2 with title "Test " & testId & " Preconditions"

tell application "Alfred 2" to search command

tell application "System Events" 
	delay 5

	keystroke tab
	
	delay 1

	keystroke tab
	
	delay 1

	keystroke task

	delay 2

	keystroke return

	delay 4

	set result to button returned of (display dialog postcondition buttons {"Pass", "Fail"} default button 1 with title "Please verify")
	if result is "Pass"
		1
	else
		0
	end if

end tell
