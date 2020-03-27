from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from audiology import db, login_manager
from flask_login import UserMixin

playlist_songs = db.Table("playlist_songs",
                          db.Column("private_playlist_id", db.Integer,
                                    db.ForeignKey("private_playlists.id")),
                          db.Column("song_id", db.Integer,
                                    db.ForeignKey("songs.id"))
                          )


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "artists.id"), nullable=True)
    artist = db.relationship("Artist", backref="albums", lazy=True)


class Song(db.Model):
    __tablename__ = "songs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    duration = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    lyrics = db.Column(db.String(255), unique=False, nullable=True)
    image_file = db.Column(db.String(255), nullable=False,
                           default='default.jpg')
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "artists.id"), nullable=False)
    artist = db.relationship("Artist", backref="songs", lazy=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=True)
    album = db.relationship("Album", backref="songs", lazy=True)

    def __rep__(self):
        return(f"Song Name: {self.name}\nSong Length: {self.duration}\nLyrics: {self.lyrics}\nArtist: {self.artist.name}\nLanguage: {self.artist.language}\nAlbum Cover: {self.image}")


class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)


class PrivatePlaylist(db.Model):
    __tablename__ = "private_playlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)

    username_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False)
    username = db.relationship("User", backref="privateplaylist", lazy=True)
    songs = db.relationship("Song", secondary=playlist_songs)
