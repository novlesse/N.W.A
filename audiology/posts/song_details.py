import requests
import json

def jsonprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def get_details(payload, song_name, artist):
    # define headers and URL
    headers = {'user-agent': 'Audiology'}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['track'] = song_name
    payload['artist'] = artist
    payload['api_key'] = '558863e8d1f0c76c81aa1448d99ed62a'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response


def get_artist_image(artist):
    headers = {'user-agent': 'Audiology'}
    url = 'http://ws.audioscrobbler.com/2.0/'
    payload = {
        'method': 'artist.getInfo'
    }
    payload['artist'] = artist
    payload['api_key'] = '558863e8d1f0c76c81aa1448d99ed62a'
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def get_track_tags(response):
    tag_list = []
    for tags in response.json()['track']['toptags']['tag']:
        tag_list.append(tags['name'])
    return tag_list


def get_album_name(response):
    if 'album' in response.json()['track']:
        return response.json()['track']['album']['title']
    else:
        return response.json()['track']['name']


def get_track_image(response):
    if 'album' in response.json()['track']:
        return response.json()['track']['album']['image'][2]['#text']
    else:
        image = get_artist_image(response.json()['track']['artist']['name'])
        return image.json()['artist']['image'][2]['#text']


def get_lyrics(payload, song, artist):
    headers = {'user-agent': 'Audiology'}
    url = 'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get'

    payload['callback'] = 'callback'
    payload['q_artist'] = artist
    payload['q_track'] = song
    payload['apikey'] = '30f56ff93aa6f5e81a505e9940dc3c87'

    response = requests.get(url, headers=headers, params=payload)
    return response.json()['message']['body']['lyrics']['lyrics_body']
