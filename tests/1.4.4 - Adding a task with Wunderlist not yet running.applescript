set testId to "1.4.4"
set task to "Sample task #workflowtest " & testId
set command to "wl to:" & task
set precondition to "Quit the Wunderlist application before proceeding."
set postcondition to "New task " & task & " added in the \"Today\" list and previous application reactivated"

display dialog precondition buttons {"Go", "Cancel"} default button 1 cancel button 2 with title "Test " & testId & " Preconditions"

tell application "Alfred 2" 
	search command

	delay 1
end tell

delay 1

tell application "System Events" 
	keystroke return

	delay 4

	set result to button returned of (display dialog postcondition buttons {"Pass", "Fail"} default button 1 with title "Please verify")
	if result is "Pass" then
		1
	else
		0
	end if

end tell
