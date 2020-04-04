import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from audiology.config import Config
from flask_dropzone import Dropzone


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
dropzone = Dropzone()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #TESTING-- start
    
    #TESTING---end

    from audiology.users.routes import users
    from audiology.posts.routes import posts
    from audiology.main.routes import main
    from audiology.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    db.init_app(app)
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()
    return app
