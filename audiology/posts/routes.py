import os
import boto3
import json
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, send_file)
from flask_login import current_user, login_required
from audiology import db
from audiology.models import Post, Album, Artist, Song, PrivatePlaylist
from audiology.posts.forms import SongForm, UpdateSongForm
from audiology.posts.audio import list_files, download_file, upload_file, get_bucket_location
from audiology.posts.song_details import (jsonprint, get_details, get_track_tags,
                                          get_track_image, get_lyrics, get_album_name,
                                          get_artist_image)

posts = Blueprint('posts', __name__)



@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = SongForm()
    if form.validate_on_submit():

        song_details = get_details({
            'method': 'track.getinfo'
        }, form.song_name.data, form.artist.data)
        song_lyrics = get_lyrics({
            'format': 'json'
        }, form.song_name.data, form.artist.data)
        song_image = get_track_image(song_details)
        song_duration = song_details.json()['track']['duration']
        song_tags = get_track_tags(song_details)

        song_file = request.files['file']
        song_file.save(os.path.join("uploads", song_file.filename))
        upload_file(f'uploads/{song_file.filename}', "audiologyfiles")
        file_location = "".join(song_file.filename.split())
        audio_path = get_bucket_location(file_location, "audiologyfiles")
        print(audio_path)
        os.remove(f'uploads/{song_file.filename}')

        artist_query = Artist.query.filter_by(name=form.artist.data).first()
        if not artist_query:
            artist = Artist(name=form.artist.data)
        else:
            artist = artist_query
        db.session.add(artist)

        if 'album' not in song_details.json()['track']:
            album_query = Album.query.filter_by(name=song_details.json()['track']['name']).first()
            album_name = song_details.json()['track']['name']
        else:
            album_query = Album.query.filter_by(
                name=song_details.json()['track']['album']['title']).first()
            album_name = song_details.json()['track']['album']['title']

        if not album_query:
            album = Album(name=album_name, 
                          year=form.year.data,
                          image_file=song_image,
                          artist=artist)
        else:
            album = album_query 
        db.session.add(album)
        song_query = Song.query.filter_by(name=form.song_name.data).first()
        if not (song_query and album_query):
            song = Song(name=form.song_name.data,
                        duration=song_duration,
                        year=form.year.data,
                        lyrics=song_lyrics,
                        audio_file=audio_path,
                        image_file=song_image,
                        artist=artist,
                        album=album)
        else:
            song = song_query
        db.session.add(song)

        playlist_query = PrivatePlaylist.query.filter_by(
            username_id=current_user.id).first()
        if not playlist_query:
            playlist = PrivatePlaylist(name=current_user.username,
                                       username=current_user)
            db.session.add(playlist) 
            playlist.songs.append(song)
        else:
            playlist = playlist_query.songs.append(song)
        
        db.session.commit()
        flash('Your song has been added.', 'success')
        return redirect(url_for("users.user_playlist", username=current_user.username))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/download/<filename>", methods=["GET"])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:song_id>/update", methods=['GET', 'POST'])
@login_required
def update_song(song_id):
    song = Song.query.get_or_404(song_id)
    form = UpdateSongForm()
    if form.validate_on_submit():
        song.name = form.song_name.data
        song.artist.name = form.artist.data
        song.lyrics = form.lyrics.data
        db.session.commit()
        flash('Song has been updated.', 'success')
        return redirect(url_for('posts.update_song', song_id=song.id))
    elif request.method == 'GET':
        form.song_name.data = song.name
        form.artist.data = song.artist.name
        form.lyrics.data = song.lyrics
    return render_template('update_song.html', title='Update Song',
                           form=form, legend='Update Song')


@posts.route("/storage") 
@login_required
def storage():
    contents = list_files("audiologyfiles")
    return render_template('storage.html', contents=contents)
