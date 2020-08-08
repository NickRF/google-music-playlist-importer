#!/usr/bin/env python

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Import a Spotify or CSV playlist in to Google Music.')
    parser.add_argument('--name', help='specify playlist name')
    parser.add_argument('--parse-only', default=False, action='store_true', help="parse (and print) input, but don't interact with Google Music")
    parser.add_argument('--dry-run', default=False, action='store_true', help="parse the input and look up songs, but don't create a Google Music playlist")
    parser.add_argument('--print-input', default=False, action='store_true', help="print the input playlist data")
    parser.add_argument('--csv', dest='csv_filename', help='specify a CSV file to export to')
    parser.add_argument('playlist', help='CSV file path or Spotify playlist URL')
    args = parser.parse_args()
    playlist = args.playlist
    dry_run = args.dry_run

    if "://open.spotify.com" in playlist:
        import ie.spotify_import
        name, data = ie.spotify_import.get_song_data(playlist)
    else:
        import ie.csv_ie
        name, data = ie.csv_ie.get_song_data(playlist)

    assert data

    if args.name:
        name = args.name

    if args.print_input or args.parse_only:
        print(name)
        print("=" * len(name))
        for row in data:
            artist, title = row
            print('%s - %s' % (artist, title))

    if args.parse_only:
        sys.exit(0)

    if False:
        #TODO: gmusicapi no longer working
        import ie.gmusic_export
        ie.gmusic_export.export_song_data(name, data, args.dry_run)
    elif args.csv_filename:
        import ie.csv_ie
        if not args.dry_run:
            ie.csv_ie.export_song_data(args.csv_filename, data)
    else:
        import ie.ytmusic_export
        ie.ytmusic_export.export_song_data(name, data, args.dry_run)
        pass
