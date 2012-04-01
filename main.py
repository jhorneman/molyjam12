import sys
import os

__author__ = 'jhorneman'

from flask import Flask, session, redirect, url_for, request, render_template, g
from data import load_data, scenes, scene_files, warnings

default_sparkle = 50

app = Flask(__name__)
app.config.from_object('molyjam_default_settings')


# (for convenience)
class User(object):
    def __init__(self):
        self.sparkle = default_sparkle


@app.route("/")
def index():
    return redirect(url_for('scene'))


@app.route("/scene/")
@app.route("/scene/<scene_name>")
def scene(scene_name='start'):
    user = User()
    if 'user_sparkle' in session:
        user.sparkle = session["user_sparkle"]

    if scenes.has_key(scene_name):
        return render_template('scene.html', scene=scenes[scene_name], user=user)
    else:
        return render_template('scene_not_found.html', user=user)


@app.route("/status")
def status():
    user = get_user()
    return render_template('status.html', user=user, warnings=warnings)


if __name__ == "__main__":
    # Dev mode
    if (len(sys.argv) == 1) or (len(sys.argv) > 1 and sys.argv[1] == "dev"):
        app.config['PORT_NR'] = 5001
        app.debug = True

    # Test mode
    elif sys.argv[1] == "test":
        app.config['PORT_NR'] = 5000
        app.debug = True

    # Production mode
    elif sys.argv[1] == "production":
        # Get port number from Heroku environment variable
        app.config['PORT_NR'] = os.environ['PORT']
        app.debug = False

    success = load_data(app.logger)
    if success:
        app.run(extra_files=scene_files, port=app.config['PORT_NR'])
