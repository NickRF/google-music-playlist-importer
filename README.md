Google Music Playlist Importer
==============================

Simple tool to convert playlist formats.

Imports:
* Spotify
* CSV

Exports:
* Google Play Music
* YouTube Music
* CSV

Spotify playlists are currently scraped from the HTML page for simplicity.

Tracks are matched to Google's music catalog using a simple artist/title search.

How to use
==========

Initial authentication setup is handled by [gmusicapi](https://github.com/simon-weber/gmusicapi) / [ytmusicapi](https://github.com/sigma67/ytmusicapi).

Examples
========

Import CSV to YouTube Music
```
./import.py filename.csv
```

Import Spotify to CSV

```
./import.py --csv playlist.csv 'https://open.spotify.com/album/0qW47WLD1WTMojO8AJXxH8'
```
