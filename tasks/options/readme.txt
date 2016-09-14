New in version <%= pkg.version %>:
  * Fixed handling of accented characters followed by a keyword 
    - für parsed as fü r which triggered the "r" reminder keyword
  * Fixed relaunching of Alfred 3 after changing a preference
    - For example, toggling completed tasks reopens Alfred with the same search
    - Alfred 2 was not affected
* Added this readme so that you can see what is changed in each update!

More details:
https://github.com/idpaterson/alfred-wunderlist-workflow/releases/tag/<%= pkg.version %>


The 0.6 series includes the following major changes:
  * Added upcoming and due screens
  * Search and browse tasks
  * New command format allowing partial commands like wls instead of wl-search
  * Complete, delete, and view tasks in Wunderlist desktop app

More details:
https://github.com/idpaterson/alfred-wunderlist-workflow/releases/tag/0.6.0