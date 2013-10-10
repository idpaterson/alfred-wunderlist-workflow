(*!
	@header     Configuration
	@abstract   Basic configurations available to users building the
	            workflow from source.
	@discussion Each of the configurations provided here is a candidate
	            for user-level configuration if it seems useful. Until
	            the workflow supports that, configurable properties will
	            be tracked here for clarity.
	@version    0.2
*)

(*!
	Determines which color theme to use for the list icons. These
	icons 

	@abstract Changes the appearance of list icons in Alfred
	@attributelist Supported Values
		light For use in dark-colored Alfred themes
		dark  For use in light-colored Alfred themes
*)
property iconTheme : "light"

(*!
	The list of tasks available in Wunderlist is cached by this workflow,
	enabling faster responses to typing in Script Filter inputs. This
	setting controls how often the cached list data is refreshed.

	@abstract Specifies how often to reload information about task lists
*)
property listCacheInSeconds : 30
