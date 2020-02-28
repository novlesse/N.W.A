class Album:

    def __init__(self, name, year, songs, cover_img, artist=None, song_list=None):
        self.name = name
        self.year = year
        self.songs = songs
        self.cover_img = cover_img
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
