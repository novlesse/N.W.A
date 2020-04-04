from flask import render_template, request, Blueprint
from audiology.models import Post, Song, PrivatePlaylist
from flask_login import login_user, current_user, logout_user, login_required
from audiology import db

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home") 
def home():
    if current_user.is_authenticated:
        user_playlist = PrivatePlaylist.query.filter_by(username_id=current_user.id).first()
        print(current_user.id)
    else:
        user_playlist = False
    page = request.args.get('page', 1, type=int)
    song_list = Song.query.order_by(Song.id.desc())
    songs = song_list.paginate(page=page, per_page=10)

    return render_template('home.html', song_list=song_list, songs=songs, playlist=user_playlist)
 


 