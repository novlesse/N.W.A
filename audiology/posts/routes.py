import os
import boto3
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, send_file)
from flask_login import current_user, login_required
from audiology import db
from audiology.models import Post, Album, Artist, Song, PrivatePlaylist
from audiology.posts.forms import PostForm
from audiology.posts.audio import list_files, download_file, upload_file
from audiology.posts.song_details import (jsonprint, get_details, get_track_tags,
                                          get_track_image, get_lyrics, get_album_name)

posts = Blueprint('posts', __name__)
# UPLOAD_FOLDER = "uploads"
# BUCKET = "audiologyfiles"

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():

        # song_file = request.files['file']
        # song_file.save(os.path.join("uploads", song_file.filename))
        # upload_file(f'uploads/{song_file.filename}', "audiologyfiles")

        song_details = get_details({
            'method': 'track.getinfo'
        }, form.song_name.data, form.artist.data)
        song_lyrics = get_lyrics({
            'format': 'json'
        }, form.song_name.data, form.artist.data)
        song_image = get_track_image(song_details)
        song_duration = song_details.json()['track']['duration']
        song_tags = get_track_tags(song_details)
        artist_query = Artist.query.filter_by(name=form.artist.data).first()
        if not artist_query:
            artist = Artist(name=form.artist.data)
        else:
            artist = artist_query
        db.session.add(artist)
        album_query = Album.query.filter_by(name=get_album_name(song_details)).first()
        if not album_query:
            album = Album(name=get_album_name(song_details),
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
                        image_file=song_image,
                        artist=artist,
                        album=album)
        else:
            song = song_query
        db.session.add(song)
        playlist_query = PrivatePlaylist.query.filter_by(username_id=current_user.id).first()
        if not playlist_query:
            playlist = PrivatePlaylist(name=current_user.username,
                                    username=current_user)
            db.session.add(playlist)
            playlist.songs.append(song)
        else:
            print(song)
            print(playlist_query.id)
            playlist = playlist_query.songs.append(song)
        db.session.commit()
        song_file = request.files['file']
        song_file.save(os.path.join("uploads", song_file.filename))
        upload_file(f'uploads/{song_file.filename}', "audiologyfiles")
        os.remove(f'uploads/{song_file.filename}')
        flash('Your post has been created.', 'success')
        return redirect(url_for('main.home'))
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


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated.', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('main.home'))

@posts.route("/storage")
@login_required
def storage():
    contents = list_files("audiologyfiles")
    return render_template('storage.html', contents=contents)



