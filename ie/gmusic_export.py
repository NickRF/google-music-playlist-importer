from gmusicapi import Mobileclient
import sys

def data_to_song_ids(gmusic, data):
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

def export_song_data(name, data, dry_run):
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

    song_ids = data_to_song_ids(gmusic, data)
    print("Found %d/%d tracks on Google Music." % (len(song_ids), len(data)))
    if song_ids and not dry_run:
        playlist_id = gmusic.create_playlist(name)
        gmusic.add_songs_to_playlist(playlist_id, song_ids)
        print("Created playlist \"%s\"." % name)
