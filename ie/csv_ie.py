import csv

# Import
def get_song_data(filename):
    """Return artist/title data from a CSV file.
    CSV file should be formatted as:

    title,artist,album
    """

    data = []
    with open('playlist.csv', 'rU') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        for row in reader:
            (title, artist, _) = row
            data.append((artist, title))
    return ('CSV Playlist', data)

# Export
def export_song_data(filename, data):
    if not filename:
        raise("No filename specified")

    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"')
        for track in data:
            writer.writerow(track)