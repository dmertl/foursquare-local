foursquare-local
================

Download your Foursquare checkins to a local database.

TODO
----

- Write oauth front end piece.
- Class to perform download/sync.
- Clean up into re-usable class.
- Create CLI.
- Support for output of transactions instead of updating database file directly.
- Front end pages for viewing local database.

Issues
------

- How do we handle updates of related records like venues?
-- Only update a venue when a checkin is downloaded linked to venue?

Summary
-------

Provides a web interface for downloading Foursquare checkin data to a local database. Can also perform basic queries
against local data. Can perform synchronization to update local database with latest Foursquare data.

Database
--------

Save to SQLite database file.

Synchronization
---------------

Find date or sequential ID of last checkin. Query for all checkins starting from that date up to current time. Add to
local database.

API
---

Provide a python class that wraps foursquare lib calls with sync logic.

CLI
---

Provide a CLI that can be used to download or sync a database file.
