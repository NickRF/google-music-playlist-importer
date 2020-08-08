from ytmusicapi import YTMusic
import os.path

AUTH_FILE = "./yt-auth.json"

def export_song_data(name, data, dry_run):
    if not os.path.exists(AUTH_FILE):
        YTMusic.setup(filepath=AUTH_FILE)

    ytmusic = YTMusic(AUTH_FILE)

    song_ids = data_to_song_ids(ytmusic, data)
    print("Found %d/%d tracks on YouTube Music." % (len(song_ids), len(data)))
    if song_ids and not dry_run:
        playlist_id = ytmusic.create_playlist(name, "Auto-generated playlist")
        ytmusic.add_playlist_items(playlist_id, song_ids)
        print("Created playlist \"%s\"." % name)

# Combine multiple artists in to one artist string
def artist_from_track(track):
    return ", ".join([a["name"] for a in track['artists']])

def data_to_song_ids(ytmusic, data):
    """Convert artist/title data to YouTube Music song IDs"""

    def best_track(results):
        """Find best track in list of search results"""

        def normalise(s):
            """Normaise artist and title strings for comparison"""
            # TODO: Handle unicode
            return s.lower().replace('(', '').replace(')', '').replace('- ', '')

        # Search for exact match (sometimes a remix appears as first result)
        for track in results:
            track_artist = artist_from_track(track)
            if normalise(track_artist) == normalise(artist) and normalise(track['title']) == normalise(title):
                return track
        # If we don't find exact match, use the first hit
        return results[0]

    song_ids = []
    for row in data:
        artist, title = row

        print("%s - %s => " % (artist, title), end='')
        r = ytmusic.search(query="%s %s" % (artist, title), filter='songs')
        if r:
            track = best_track(r)
            print("%s - %s" % (artist_from_track(track), track['title']))
            song_ids.append(track['videoId'])
        else:
            print("Not found!")

    return song_ids
