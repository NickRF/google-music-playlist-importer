#!/usr/bin/env python

from gmusicapi import Mobileclient
import sys


def get_csv(filename):
    """Return artist/title data from a CSV file.
    CSV file should be formatted as:

    title,artist,album
    """

    import csv

    data = []
    with open('playlist.csv', 'rU') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            (title, artist, album) = row
            data.append((artist, title))
    return ('CSV Playlist', data)


def get_spotify(url):
    """Returns artist,title info scraped from the specified Spotify playlist URL"""

    from lxml import html
    import requests

    page = requests.get(url)
    tree = html.fromstring(page.content)

    name = tree.xpath('//h1/span//text()')[0]
    tracks = tree.xpath('//span[@class="track-name"]/text()')
    artists = tree.xpath('//span[@class="artists-albums"]/a[contains(@href,"/artist/")][1]/span/text()')

    assert len(tracks) == len(artists)

    # For some reason, HTML entities are double-escaped, so unescape again...
    name = html.fromstring(name).text
    tracks = [html.fromstring(t).text for t in tracks]
    artists = [html.fromstring(a).text for a in artists]

    return (name, zip(artists, tracks))


def data_to_song_ids(data):
    """Convert artist/title data to Google Music song IDs"""

    def best_track(results):
        """Find best track in list of search results"""

        def normalise(s):
            """Normaise artist and title strings for comparison"""
            # TODO: Handle unicode
            return s.lower().replace('(', '').replace(')', '').replace('- ', '')

        # Search for exact match (sometimes a remix appears as first result)
        for hit in results:
            track = hit['track']
            if normalise(track['artist']) == normalise(artist) and normalise(track['title']) == normalise(title):
                return track
        # If we don't find exact match, use the first hit
        return results[0]['track']

    song_ids = []
    for row in data:
        artist, title = row

        r = gmusic.search("%s %s" % (artist, title), max_results=5)['song_hits']
        if r:
            track = best_track(r)
            song_ids.append(track['storeId'])
        else:
            print("Not found: %s - %s" % (artist, title))

    return song_ids


if __name__ == "__main__":
    playlist = sys.argv[1]
    print_data = False
    dry_run = False

    if "://open.spotify.com" in playlist:
        name, data = get_spotify(playlist)
    else:
        name, data = get_csv(playlist)

    assert data

    if print_data:
        print(name)
        print("=" * len(name))
        for row in data:
            artist, title = row
            print('%s - %s' % (artist, title))

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
    if song_ids and not dry_run:
        playlist_id = gmusic.create_playlist(name)
        gmusic.add_songs_to_playlist(playlist_id, song_ids)
        print("Created playlist \"%s\"." % name)
