class User:
    def __init__(self):
        self.__first_name = ""
        self.__last_name = ""

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name
    
    @first_name.setter
    def first_name(self, value):
        self.__first_name = value

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    def make_playlist(self, name):
        self.private_playlist = PrivatePlaylist(name)

    def remove_playlist(self, name):
        del name


class Album:
    def __init__(self, name, year, cover_img):
        self.album_name_holder = name
        self.name = name
        self.year = year
        self.cover_img = cover_img
        self.song_list = []

    def add_song(self, name, duration, lyrics, artist_name, language):
        # Compositional instantiation
        self.song = Song(name, duration, lyrics, artist_name, language)
        self.song_list.append(self.song)
        # If the song length = 1, the album will be the name of the song. Else, name will be the instantiated name
        if len(self.song_list) == 1:
            self.name = self.song.name
            self.song.image = None
        else: 
            self.name = self.album_name_holder
            self.song.image = self.cover_img

    def remove_song(self, remove):
        remove = remove - 1
        self.song_list.pop(remove)

        if len(self.song_list) == 1:
            self.name = self.song.name
            self.song.image = None
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
    def __init__(self, name, language="English", albums=1):
        self.name = name
        self.language = language
        self.album_amount = albums
    

class PrivatePlaylist: 
    def __init__(self, name):
        self.name = name
        self.songs = []
    
    def add_song(self, song):
        self.song = song
        self.songs.append(self.song)

    def remove_song(self, remove):
        remove = remove - 1
        self.songs.pop(remove)

    def show_songs_in_playlist(self):
        print("Your playlist contains the following song(s):\n")
        for song in self.songs:
            # song.song refers to each song inside the self.songs list and referring to self.song inside the Album class (line 39)
            print(song.song, "\n")
    

# Instantiate Album and add song.
first_album = Album("Jeff's Album", 2020, "Jeff's Album Cover")
first_album.add_song("Jeff's song", "300s", "These are my lyrics", "Jeff", "English")


# Instantiate User and make a private playlist (compositional relationship) using make_playlist method. 
john = User()
john.first_name = "John"
john.last_name = "Nguy"

# We instantiate PrivatePlaylist class using method belonging to User class called make_playlist (Line 22).
john.make_playlist("John's playlist")

# Now instance of User has access to instance of PrivatePlaylist methods. 
# PrivatePlaylist class is instantiated as self.private_playlist inside the User class (See line 23).

# We call the add_song method that we now have access to, adding our "single" first_album. 
john.private_playlist.add_song(first_album)

# this is calling the method inside PrivatePlaylist class to show all songs inside that playlist
john.private_playlist.show_songs_in_playlist()








#
# Delete these prints if you want to... but they will be helpful if the code is confusing.. composition is confusing af.
#



# print(first_album.song_list)
# print("Album name:", first_album.name)
# print("Song image:", first_album.song.image, "\n")

# Uncomment following lines to see that adding more than one song to album changes:
# song name -> album name   and song image -> becomes album image.

# first_album.add_song("Jeff's song2", "300s", "These are my lyrics", "Jeff", "English")
# print(len(first_album.song_list))
# print("Album name:", first_album.name)
# print("Song image:", first_album.song.image, "\n")
# first_album.remove_song(2)
# print(len(first_album.song_list))

# print("Album name:", first_album.name)
# print("Song image:", first_album.song.image)

