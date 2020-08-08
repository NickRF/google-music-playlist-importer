from lxml import html
import requests

def get_song_data(url):
    """Returns artist,title info scraped from the specified Spotify playlist URL"""

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

    return (name, list(zip(artists, tracks)))