from lxml import html
import requests

def get_song_data(url):
    """Returns artist,title info scraped from the specified Spotify playlist URL

    Note: HTML content varies depending on browser detected.
    Content will likely differ here from that fetched in a modern browser"""

    page = requests.get(url)
    tree = html.fromstring(page.content)

    name = tree.xpath('//h1/span//text()')[0]
    tracks = tree.xpath('//span[@class="track-name"]/text()')
    artists = tree.xpath('//span[@class="artists-albums"]/a[contains(@href,"/artist/")][1]/span/text()')

    # If there's no artist info for each track (e.g. if this is an album), populate with album artist
    if not artists:
        album_artist = tree.xpath('//h2/a[starts-with(@href,"/artist/")]/text()')[0]
        artists = [album_artist] * len(tracks)

    assert len(tracks) == len(artists)

    # For some reason, HTML entities are double-escaped, so unescape again...
    name = html.fromstring(name).text
    tracks = [html.fromstring(t).text for t in tracks]
    artists = [html.fromstring(a).text for a in artists]

    return (name, list(zip(artists, tracks)))