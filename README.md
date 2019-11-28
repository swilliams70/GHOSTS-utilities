# GHOSTS-utilities
Utilities to help develop/manage content for the excellent GHOSTS cyber range NPC automation project. This is an independent contribution, author has no offfical association with CMU.

GHOSTS can be found here:
https://github.com/cmu-sei/GHOSTS

Changes:
=========
11/26/19: initial commit of timeline editor and timeline parser (timeline visualization solution - initially developed with plotly)
11/27/19: Changed tlparse to use matplotlib and tkinter. This will allow the tleditor and tlparser to converge into one app in future.

Issues:
================
Times cannot end at 24:00:00, various python libraries don't like this. Use 23:59:59 instead. Hardcode the conversion?

Parser doesn't render times on x axis well. Issue with matplotlib datetime object vs python datetime object?
https://matplotlib.org/3.1.1/api/dates_api.html#matplotlib.dates.date2num

Parser clips some handler names to the left of y axis.

File test.json is hardcoded in parser.

