#!/usr/bin/env python

import csv
from ConfigParser import ConfigParser
from gmusicapi import Mobileclient

config = ConfigParser()
config.read("config.ini")

username = config.get("login", "username")
password = config.get("login", "password")

gmusic = Mobileclient()
logged_in = gmusic.login(username, password)

assert logged_in, "Can't login"

with open('playlist.csv', 'rU') as csv_file:
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    song_ids = []
    for row in reader:
        (title, artist, album) = row
        # print '%s - %s' % (artist, title)
        r = gmusic.search_all_access("%s %s" %(artist,title), max_results=1)['song_hits']
        if r:
            song_ids.append(r[0]['track']['nid'])
            # print '%s - %s' % (track['artist'],track['title'])
        else:
            print "Not found: %s - %s" % (artist, title)

playlist_id = gmusic.create_playlist('Imported Playlist')
gmusic.add_songs_to_playlist(playlist_id, song_ids)

