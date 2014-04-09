set testId to "4.2.1"
set task to "Sample task #workflowtest " & testId
set command to "wl star:" & task
set precondition to "Select any custom list in Wunderlist then press Cmd+M to minimize the main window. Activate a different app on the same desktop before pressing Go. Wunderlist should be running on the same desktop but with no visible windows."
set postcondition to "New task " & task & " added in the \"Starred\" list and previous application reactivated"

display dialog precondition buttons {"Go", "Cancel"} default button 1 cancel button 2 with title "Test " & testId & " Preconditions"

tell application "Alfred 2" to search command

delay 2

tell application "System Events" 
	tell process "Alfred 2" to keystroke return

	delay 5

	set result to button returned of (display dialog postcondition buttons {"Pass", "Fail"} default button 1 with title "Please verify")
	if result is "Pass"
		1
	else
		0
	end if

end tell
