Google Music Playlist Importer
==============================

Simple tool to import Spotify or CSV playlists in to your Google Music account.

Spotify playlists are currently scraped from the HTML page for simplicity.

Tracks are matched to Google Music's catalog using a simple search of Artist + Title.

How to use
==========

To use, run:

`./import.py filename.csv`

or

`./import.py 'https://open.spotify.com/...'`

When running for the first time, you will be directed to Google to obtain an authentication token. This will be stored for future runs.
