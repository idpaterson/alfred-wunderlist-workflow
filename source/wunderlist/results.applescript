(*!
	@header     Alfred Results
	@abstract   Utilities for displaying results in Alfred.
	@discussion
	@version    0.2
*)

(*!
	@abstract Adds a result to Wunderlist based on the workflow's
	localization for the provided key.
	@param theKey:theKey The localization key supporting Title and Details
	@param theUid:theUid The uid of the result for ordering by frequency of use
	in Alfred, should be unique or `missing value` to maintain the order in
	which results are sent to Alfred.
	@param theArg:theArg The argument that will be passed on
	@param theIcon:theIcon The icon to use for the result item
	@param isValid:isValid Sets whether the result item can be actioned
	@param theAutocomplete:theAutocomplete The autocomplete value for the result item
*)
on addResultWithLocalization given theKey:theKey, theUid:theUid, theArg:theArg, theIcon:theIcon, theAutocomplete:theAutocomplete, theType:theType, isValid:isValid

	# Load localizations
	set theTitle to l10n(theKey & "/Title")
	set theSubtitle to l10n(theKey & "/Details")

	tell getCurrentWorkflow()
		add_result given theUid:theUid, theArg:theArg, theTitle:theTitle, theSubtitle:theSubtitle, theIcon:theIcon, theAutocomplete:theAutocomplete, theType:theType, isValid:isValid
	end tell

end addResultWithLocalization

(*!
	@abstract Adds a result to Alfred that allows the task to be added to
	the list that is currently active in Wunderlist.
	@param query The complete Alfred query
*)
on addResultForInsertingTaskInActiveList(query)

	# TODO: show the name of the active list so that there is no doubt which
	# will receive the task.
	addResultWithLocalization with isValid given theKey:"Results/Add task to active list", theUid:missing value, theArg:query, theIcon:"icon.png", theAutocomplete:missing value, theType:missing value
	
end addResultForInsertingTaskInActiveList

