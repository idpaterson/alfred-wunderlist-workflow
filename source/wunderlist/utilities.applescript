(*!
	@header     Utilities
	@abstract   A collection of useful functions.
	@version    0.2
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
	@functiongroup Alfred Helpers
*)

# The current workflow created by qWorkflow
property workflow : missing value

# The path to this workflow within Alfred's preferences bundle
property workflowFolder : missing value

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
	@abstract Provides access to the current workflow constructed by qWorkflow.
	@return The workflow constructed by qWorkflow's <code>new_workflow</code>
*)
on getCurrentWorkflow()
	if workflow is missing value then
		set workflow to new_workflow()
	end if 

	return workflow
end getCurrentWorkflow

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

(*!
	@functiongroup Algorithms
*)

(*!
	@abstract   An implementation of the quick sort algorithm for simple
	comparable data types (string, number, date).
	@discussion Internally, this uses @link quickSortWithKeyHandler @/link
	with the default key handler that causes the values of the list to be
	sorted directly.
	@param theList A list of simple comparable values (string, number, date)
	@see quickSortWithKeyHandler
*)
on quickSort(theList)
	return quickSortWithKeyHandler(theList, missing value)
end quickSort

(*!
	@abstract   An implementation of the quick sort algorithm that allows
	a key to be extracted from complex data types with a handler.
	@discussion This implementation of quick sort selects a starting pivot
	in the middle of the list to ensure optimal sorting of lists that are
	already partially sorted. Values are sorted in ascending order.
	Consider the following example:
	<pre><code>    set fruits to {{name:"Kumquat", color:"orange"},{name:"Apple", color:"red"},{name:"Lychee", color:"pink"}}

    on getFruitName(fruitInfo)
	    return name of fruitInfo
    end getFruitName

    set fruits to quickSortWithKeyHandler(fruits, getFruitName)</code></pre>
    @attributeblock Acknowledgements
    This handler is based on code for the quick sort algorithm provided by
    <a href="http://macscripter.net/viewtopic.php?id=24766" target="_blank">
    Kevin Bradley at MacScripter</a>.
	@param theList A list of simple comparable values (string, number, date)
	or complex types such as records and nested lists. The latter must be
	accompanied by a <code>keyHandler</code> to extract a comparable value
	for sorting.
	@param keyHandler A handler that when given a value from 
	<code>theList</code> returns the value on which that item should be
	sorted. If <code>keyHandler</code> is <code>missing value</code> then
	the values in the list will be sorted directly.
*)
on quickSortWithKeyHandler(theList, keyHandler)
	script bs
		property alist : theList
		property getKey : keyHandler

		on defaultKeyHandler(theValue)
			return theValue
		end defaultKeyHandler

		if getKey is missing value then
			set getKey to defaultKeyHandler
		end if
		
		on Qsort(leftIndex, rightIndex)
			if rightIndex > leftIndex then
				set pivot to ((rightIndex - leftIndex) div 2) + leftIndex
				set newPivot to Qpartition(leftIndex, rightIndex, pivot)
				set theList to Qsort(leftIndex, newPivot - 1)
				set theList to Qsort(newPivot + 1, rightIndex)
			end if
		end Qsort
		
		on Qpartition(leftIndex, rightIndex, pivot)
			set pivotValue to getKey(item pivot of bs's alist)
			set temp to item pivot of bs's alist
			set item pivot of bs's alist to item rightIndex of bs's alist
			set item rightIndex of bs's alist to temp
			set tempIndex to leftIndex
			repeat with pointer from leftIndex to (rightIndex - 1)
				if getKey(item pointer of bs's alist) ² pivotValue then
					set temp to item pointer of bs's alist
					set item pointer of bs's alist to item tempIndex of bs's alist
					set item tempIndex of bs's alist to temp
					set tempIndex to tempIndex + 1
				end if
			end repeat
			set temp to item rightIndex of bs's alist
			set item rightIndex of bs's alist to item tempIndex of bs's alist
			set item tempIndex of bs's alist to temp
			
			return tempIndex
		end Qpartition	
	end script
	
	if length of bs's alist > 1 then bs's Qsort(1, length of bs's alist)

	return bs's alist
end quickSort

