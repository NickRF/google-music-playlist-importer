#!/usr/bin/env python

from gmusicapi import Mobileclient
import sys

#from gmusicapi.utils import utils
#print utils.log_filepath

def get_csv(filename):
    import csv

    data = []
    with open('playlist.csv', 'rU') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            (title, artist, album) = row
            data.append((artist, title))
    return ('CSV Playlist', data)

def get_spotify(url):
    from lxml import html
    import requests

    page = requests.get(url)
    tree = html.fromstring(page.content)

    name = tree.xpath('//h1/span//text()')[0]
    tracks = tree.xpath('//span[@class="track-name"]/text()')
    artists = tree.xpath('//span[@class="artists-albums"]/a[contains(@href,"/artist/")][1]/span/text()')

    assert len(tracks) == len(artists)

    return (name, zip(artists, tracks))

def data_to_song_ids(data):
    song_ids = []
    for row in data:
        artist, title = row

        r = gmusic.search("%s %s" %(artist,title), max_results=1)['song_hits']
        if r:
            song_ids.append(r[0]['track']['storeId'])
        else:
            print("Not found: %s - %s" % (artist, title))

    return song_ids

playlist = sys.argv[1]
print_data = False
dry_run = False

if "://open.spotify.com" in playlist:
    name, data = get_spotify(playlist)
else:
    name, data = get_csv(playlist)

if print_data:
    print(name)
    print("=" * len(name))
    for row in data:
        artist, title = row
        print('%s - %s' % (artist, title))

if data and not dry_run:
    gmusic = Mobileclient()
    logged_in = gmusic.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
    if not logged_in:
        print("Couldn't log in. Starting authentication...")
        gmusic.perform_oauth()
        logged_in = gmusic.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        if logged_in:
            print("Logged in!")
        else:
            print("Login failed.")
            sys.exit(1)

    song_ids = data_to_song_ids(data)
    print("Found %d/%d tracks on Google Music." % (len(song_ids), len(data)))
    if song_ids:
        playlist_id = gmusic.create_playlist(name)
        gmusic.add_songs_to_playlist(playlist_id, song_ids)
        print("Created playlist \"%s\"." % name)

