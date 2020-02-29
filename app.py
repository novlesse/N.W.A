class Album:
    def __init__(self, name=None, year, cover_img):
        self.name = name
        self.year = year
        # self.songs = songs
        self.cover_img = cover_img
        # self.artist = songs.artist.name
        self.song_list = []
    def add_song(self, name, duration, lyrics, artist_name, language):
        self.song = Song(name, duration, lyrics, artist_name, language)
        self.song_list.append(self.song)



class Song:
    def __init__(self, name, duration, lyrics, album=None):
        self.name = name
        self.duration = duration
        self.lyrics = lyrics
        # self.artist = Artist(artist_name, language)
        self.image = album
    # def add_to_album(self, album, song):
    #     self.album = album
    #     self.album.song_list.append(song)
    def __repr__(self):
        return(f"Song Name: {self.name}\nSong Length: {self.duration}\nLyrics: {self.lyrics}\nArtist: {self.artist.name}\nLanguage: {self.artist.language}")
class Artist: 
    def __init__(self, name, language="English", albums = 1):
        self.name = name
        self.language = language
        self.albums = []

class Playlist: 
    def __init__(self, name, songs = 0):
        self.name = name
        self.songs = []

# jeff = Artist("Jeff")
# print(jeff.language, jeff.name)
first_song = Song("Jeff's song", 4, "This is a good song", "Jeff", "English")
# print(first_song)
first_album = Album("Jeff's Album", 2020, "Jeff's Album Cover")
first_album.add_existing_song(first_song)
print(first_album.song_list)