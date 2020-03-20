from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import sqlite3
from sqlite3 import Error
from flask import g
import os.path

# DATABASE = 'path'
# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        cur = conn.cursor()
        who = "Yeltsin"
        age = 72
        cur.execute("create table people (name_last, age)")
        cur.execute("insert into people values (?, ?)", (who, age))
        print('its in database')
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

app = Flask(__name__)

# @app.route('/')
# def hello():
#     message = 'this is a song'
#     return render_template('index.html', message=message)



if __name__ == '__main__':
    create_connection("/Users/macjohnalds/desktop/oop/project/n.w.a/music.db")
    app.run()0