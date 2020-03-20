from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applemusic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return (f"Name: {self.username}\n Email: {self.email}\n Password: {self.password}")

    def __hash__(self):
        return hash(self.username)

    def make_playlist(self, username):
        self.private_playlist = PrivatePlaylist(username)

    def remove_playlist(self):
        del self.private_playlist


class Album(db.Model):
    #def __init__(self, name, year, cover_img):
    __tablename__ = "albums"
    
    #name = db.Column(db.String(50), )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    #cover_img = db.Column(db.BLOB, nullable=True, default="default.jpg")
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)
    artist = db.relationship("Artist", backref="albums",lazy=True)


    # def add_song(self, name, duration, lyrics, artist_name):
    #     # Compositional instantiation
    #     self.song = Song(name, duration, lyrics, artist_name)
    #     self.song_list.append(self.song)
        # If the song length = 1, the album will be the name of the song. Else, name will be the instantiated name
        # if len(self.song_list) == 1:
        #     self.name = self.song.name
        #     self.song.image = None
        # else: 
        #     self.name = self.album_name_holder
        #     self.song.image = self.cover_img

    # def remove_song(self, remove):
    #     remove = remove - 1
    #     self.song_list.pop(remove)

    #     if len(self.song_list) == 1:
    #         self.name = self.song.name
    #         self.song.image = None
    #     else: 
    #         self.name = self.album_name_holder
    #         self.song.image = self.cover_img


# class Single(db.Model):
#     #def __init__(self, name, year, cover_img):
#     __tablename__ = "singles"
    
#     # name = db.Column(db.String(50), )
#     id = db.Column(db.Integer, primary_key=True)
#     # name = db.Column(db.String(50), unique=False, nullable=False)
#     # name_id = db.relationship("Song", primaryjoin="and_(Single.id==Song.single_id)")
#     year_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
#     year = db.relationship("Song",backref="singles_year", lazy=True)
#     #cover_img = db.Column(db.BLOB, nullable=True, default="default.jpg")
#     artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=True)
#     artist = db.relationship("Artist", backref="singles_artist",lazy=True)


class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    lyrics = db.Column(db.String(255), unique=False, nullable=False)
    # image = db.Column(db.BLOB, nullable=False, default="default.jpg")
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    artist = db.relationship("Artist", backref="songs",lazy=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=True)
    album = db.relationship("Album", backref="songs",lazy=True)
    # single_id = db.Column(db.Integer, db.ForeignKey("singles.id"), nullable=True)
    # single = db.relationship("Single", backref="songs",lazy=True)


    def __rep__(self):
        return(f"Song Name: {self.name}\nSong Length: {self.duration}\nLyrics: {self.lyrics}\nArtist: {self.artist.name}\nLanguage: {self.artist.language}\nAlbum Cover: {self.image}")


class Artist(db.Model): 
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)


class PrivatePlaylist(db.Model): 
    __tablename__ = "private_playlist"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    username_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    username = db.relationship("User", backref="privateplaylist", lazy=True)
    # def __init__(self, name):
    #     self.name = name
    #     self.songs = []
    
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



db.create_all()

john = User(username="John", email="john@hotmail.com", password="1234")
db.session.add(john)


singer = Artist(name="Jeff")
db.session.add(singer)


# Instantiate Album and add song.
first_album = Album(name="Jeff", year=2020, artist=singer)
print(first_album.artist.name)
#first_album.add_song("Jeff's song", "300s", "These are my lyrics", "Jeff", "English")
db.session.add(first_album)

song = Song(name="Happy", duration=300, year=2020, lyrics='Happyyyier', artist=singer, album=first_album)
db.session.add(song)

# Instantiate Album and add song.

# first_single = Single(name=[song], artist=singer)
# print(first_single.name)
# db.session.add(first_single)

# song = Song(name="Happy", duration=300, year=2020, lyrics='Happyyyier', artist=singer, album=first_album)
# db.session.add(song)

# song = Song(name="Happy", duration=300, year=2020, lyrics='Happyyyier', artist= singer, album=first_album)
# db.session.add(song)

# Instantiate Private Playlist
playlist_name = PrivatePlaylist(name="Emmy's Playlist", username=john)
print(playlist_name.username.username)
#playlist_name.add_song("Emmy's Song")
db.session.add(playlist_name)

db.session.commit()





































































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

