(*!
	@header     Utilities
	@abstract   A collection of useful functions.
*)

(*!
	@functiongroup Localization
*)

(*!
	@abstract Returns the most appropriate translation of the specified string
	according to the workflow's bundle.
	@discussion This workflow uses a simple hierarchical structure for localization
	to keep the keys organized and consistent. This means that the keys are not 
	suitable for display as with simple <code>"Foo" = "Foo";</code> translation by
	word or phrase. As a result, if the key is not localized, the handler will
	return <code>missing value</code>.

	@param key the string to localize, see <code>Localizable.strings</code> within 
	this workflow for available values
	@return The localized string for the given key, or <code>missing value</code>
	if a value was not found for the key
*)
on l10n(key)
	set localized to localized string of key in bundle getWorkflowFolder()
	
	if localized = key then set localized to missing value

	return localized
end l10n

(*!
	@abstract   Returns the most appropriate translation of the specified string
	according to the localization of the Wunderlist application.
	@param key the string to localize, see <code>Localizable.strings</code> within
	the Wunderlist application bundle for available values and translations
	@return The localized string for the given key, or the key itself if no
	localization was found.
*)
on wll10n(key)
	return appl10n(key, "Wunderlist", "Localizable")
end l10n

(*!
	@abstract   Returns the most appropriate translation of the specified string
	according to the localization of the specified application.
	@param key the string to localize, see <code>Localizable.strings</code> within
	the application bundle for available values and translations
	@param appName the name of the application from which to collect a localization
	@param tableName the name of the strings file from which to load the translation
	without the extension. For example, use <code>"Localizable"</code> to reference
	<em>Example.app/Contents/Resources/en.lproj/Localizable.strings</em>
	@return The localized string for the given key, or the key itself if no
	localization was found.
*)
on appl10n(key, appName, tableName)
	tell application appName
		return localized string key from table tableName
	end tell
end l10n

(*!
	@functiongroup Filesystem
*)

(*!
	@abstract Returns the path to the workflow folder within Alfred preferences.
	@return The path to the workflow folder within Alfred preferences.
*)
on getWorkflowFolder()
	if workflowFolder is missing value then
		set workflowFolder to do shell script "pwd"
	end if

	return workflowFolder
end getWorkflowFolder

(*!
	@functiongroup Alfred Helpers
*)

(*!
	@abstract   Displays a notification in Notification Center.
	@discussion Loads Title, Message, and Details text from the workflow's
	localization and uses the strings to display a Notification Center
	notification to the user. Any combination of those subkeys may be 
	specified in the localization.

	@param key a <code>Messages/</code> localization key as specified in 
	<code>Localizable.strings</code>
*)
on sendNotification(key)

	set theMessage to l10n(key & "/Title")
	set theDetails to l10n(key & "/Message")
	set theExtra to l10n(key & "/Details")

	q_send_notification(theMessage, theDetails, theExtra)

end sendNotification

