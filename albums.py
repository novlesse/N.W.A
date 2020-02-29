class Album:
    def __init__(self, name, year, cover_img):
        self.album_name_holder = name
        self.name = name
        self.year = year
        self.cover_img = cover_img
        self.song_list = []

    def add_song(self, name, duration, lyrics, artist_name, language):
        self.song = Song(name, duration, lyrics, artist_name, language)
        self.song_list.append(self.song)
        # If the song length = 1, the album will be the name of the song. Else, name will be the instantiated name
        if len(self.song_list) == 1:
            self.name = self.song.name
        else: 
            self.name = self.album_name_holder
            self.song.image = self.cover_img
        
class Song:
    def __init__(self, name, duration, lyrics, artist_name, language, image=None):
        self.name = name
        self.duration = duration
        self.lyrics = lyrics
        self.artist = Artist(artist_name, language)
        self.image = image

    def __repr__(self):
        return(f"Song Name: {self.name}\nSong Length: {self.duration}\nLyrics: {self.lyrics}\nArtist: {self.artist.name}\nLanguage: {self.artist.language}\nAlbum Cover: {self.image}")


class Artist: 
    def __init__(self, name, language="English", albums = 1):
        self.name = name
        self.language = language
        self.albums = []


class Playlist: 
    def __init__(self, name, songs = 0):
        self.name = name
        self.songs = []

# Instantiate Album and add song.
first_album = Album("Jeff's Album", 2020, "Jeff's Album Cover")
first_album.add_song("Jeff's song", "300s", "These are my lyrics", "Jeff", "English")

print(first_album.song_list)
print("Album name:", first_album.name)
print("Song image:", first_album.song.image)

# Uncomment line 54 to see that adding more than one song to album changes:
# song name -> album name   and song image -> becomes album image.

# first_album.add_song("Jeff's song2", "300s", "These are my lyrics", "Jeff", "English")

print("Album name:", first_album.name)
print("Song image:", first_album.song.image)

# Test