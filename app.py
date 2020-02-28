class Album:
    def __init__(self, name, year, songs, cover_img, language, artist=None, song_list=None):
        self.name = name
        self.year = year
        self.songs = songs
        self.cover_img = cover_img
        self.language = language
        if artist is None:
            self.artist = Artist("Album Artists")
        else:
            self.artist = artist
        self.song_list = []

    def add_song(self, song, position=None):
        if position is None:
            self.song_list.append(song)
        else:
            self.song_list.insert(position, song)


class Song:
    def __init__(self, name, duration, lyrics, artist_name, language, album_name, cover_img, year, song):
        self.name = name
        self.duration = duration
        self.lyrics = lyrics
        self.artist = Artist(artist_name, language)
        self.image = Album(album_name, cover_img, year, song)


class Artist:
    def __init__(self, name, language="English", albums=1):
        self.name = name
        self.language = language
        self.albums = []

    def add_album(self, album):
        self.albums.append(album)


class Playlist:
    def __init__(self, name, songs=0):
        self.name = name
        self.songs = []
