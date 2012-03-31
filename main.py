__author__ = 'jhorneman'

from flask import Flask, session, redirect, url_for, escape, request, render_template, g
import sqlite3
from contextlib import closing
import logging
from data import load_data, scenes, scene_files

app = Flask(__name__)
app.config.from_object('molyjam_default_settings')

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

class User(object):
    def __init__(self):
        self.name = "Unknown One"
        self.sparkle = 0

    @staticmethod
    def from_id(_user_id):
        new_user = User()
        db_data = query_db('select * from users where id = ?', [session['userid']], one=True)
        if db_data:
            new_user.name = db_data['name']
            new_user.sparkle = db_data['sparkle']
        return new_user


def get_user():
    if 'userid' in session:
        return User.from_id(session['userid'])
    else:
        new_user = User()
        new_user.name = "Untraceable One"
        return new_user

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'userid' in session:
        return redirect(url_for('scene'))

    if request.method == 'POST':
        user = query_db('select * from users where name = ?', [request.form['username']], one=True)
        if user is None:
            g.db.execute("insert into users (name, sparkle) values (?, ?)", (request.form['username'], 50))
            g.db.commit()
            #TODO: Find a nicer way of doing this
            user = query_db('select * from users where name = ?', [request.form['username']], one=True)
            session['userid'] = user['id']
        else:
            session['userid'] = user['id']
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    # remove the user ID from the session if its there
    session.pop('userid', None)
    return redirect(url_for('index'))

@app.route("/scene/")
@app.route("/scene/<scene_name>")
def scene(scene_name='start'):
    user = get_user()
#    relative_scene_image_path = url_for('static', filename='scene-images/')
    return render_template('scene.html', scene=scenes[scene_name], user=user)


if __name__ == "__main__":
    success = load_data()
    if success:
        app.logger.log(logging.DEBUG, "Successfully loaded data")
        app.run(extra_files=scene_files, port=app.config['PORT_NR'])
    else:
        app.logger.log(logging.CRITICAL, "Could not load data - aborting")
