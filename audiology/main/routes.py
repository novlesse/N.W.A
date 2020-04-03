from flask import render_template, request, Blueprint
from audiology.models import Post, Song

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home") 
def home():
    page = request.args.get('page', 1, type=int)
    songs = Song.query.order_by(
        Song.id.desc()).paginate(page=page, per_page=10)
    return render_template('hometest.html', songs=songs)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
 

@main.route("/songs")  
def playlist():
    # page = request.args.get('page', 1, type=int)
    # songs = 
    return render_template('user_posts.html', title='Playlist')
 