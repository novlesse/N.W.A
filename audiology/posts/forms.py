from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    song_name = StringField('Song Name', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    year = StringField('Song Year', validators=[DataRequired()])
    submit = SubmitField('Post')
