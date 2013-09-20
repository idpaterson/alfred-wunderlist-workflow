(*!
	@header     Alfred Results
	@abstract   Utilities for displaying results in Alfred.
	@discussion
*)

(*!
	@abstract Adds a result to Wunderlist based on the workflow's
	localization for the provided key.
	@param theKey The localization key supporting Title and Details
	@param theArg The argument that will be passed on
	@param theIcon The icon to use for the result item
	@param isValid Sets whether the result item can be actioned
	@param theAutocomplete The autocomplete value for the result item
*)
on addResultWithLocalization given theKey:_key, theUid:_uid, theArg:_arg, theIcon:_icon, theAutocomplete:_autocomplete, theType:_type, isValid:_valid

	# Load localizations
	set _title to l10n(_key & "/Title")
	set _subtitle to l10n(_key & "/Details")

	tell getCurrentWorkflow() to add_result given theUid:_uid, theArg:_arg, theTitle:_title, theSubtitle:_subtitle, theIcon:_icon, theAutocomplete:_autocomplete, theType:_type, isValid:_valid

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

