import sys
import os

__author__ = 'jhorneman'

from flask import Flask, session, redirect, url_for, request, render_template, g
from data import load_data, scenes, scene_files, warnings, get_trans_option

default_sparkle = 1
page_title = "Coin of Destiny"

app = Flask(__name__)
app.config.from_object('molyjam_default_settings')


# (for convenience)
class User(object):
    def __init__(self):
        self.sparkle = default_sparkle


@app.route("/")
def index():
    return redirect(url_for('scene'))


@app.route("/restart")
def restart():
    session["user_sparkle"] = default_sparkle
    session.pop("previous_scene")
    return redirect(url_for('scene'))


@app.route("/scene/")
@app.route("/scene/<scene_name>")
def scene(scene_name='start'):
    user = User()
    if 'user_sparkle' in session:
        user.sparkle = int(session["user_sparkle"])

    trans_text = ""
    if 'previous_scene' in session:
        trans_option = get_trans_option(scene_name, session["previous_scene"])
        if trans_option:
            trans_text = trans_option.trans_text
            user.sparkle += trans_option.sparkle_delta
            if user.sparkle < 0:
                user.sparkle = 0

    session["user_sparkle"] = str(user.sparkle)
    session["previous_scene"] = scene_name

    if scenes.has_key(scene_name):
        return render_template('scene.html', scene=scenes[scene_name], trans_text=trans_text, user=user, page_title=page_title)
    else:
        return render_template('scene_not_found.html', user=user, page_title=page_title)


@app.route("/status")
def status():
    return render_template('status.html', warnings=warnings, page_title=page_title)


if __name__ == "__main__":
    app.debug = True
    host = '127.0.0.1'

    # Dev mode
    if (len(sys.argv) == 1) or (len(sys.argv) > 1 and sys.argv[1] == "dev"):
        app.config['PORT_NR'] = 5001
        page_title += " (Jurie's dev mode)"

    # Test mode
    elif sys.argv[1] == "test":
        app.config['PORT_NR'] = 5000
        page_title += " (team test mode)"

    # Production mode
    elif sys.argv[1] == "production":
        # Get port number from Heroku environment variable
        app.config['PORT_NR'] = int(os.environ['PORT'])
        app.debug = False
        host = '0.0.0.0'

    success = load_data(app.logger)
    if success:
        app.run(extra_files=scene_files, port=app.config['PORT_NR'], host=host, debug=app.debug)
