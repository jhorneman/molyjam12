__author__ = 'jhorneman'

from flask import Flask, session, redirect, url_for, escape, request, render_template
from data import load_data, scenes, scene_files

app = Flask(__name__)

user_data = {}

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('scene'))
    return "You are not logged in"

@app.route("/scene/")
@app.route("/scene/<scene_name>")
def scene(scene_name='start'):
    return render_template('scene.html', description=scenes[scene_name][0], options=scenes[scene_name][1])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# set the secret key.  keep this really secret:
app.secret_key = 'n\x86\xd4\x85\xcevqe\x82\xc1K\xc6|\x00\x0fl\xcf\x16\t\x9a\xa0QB\xf2'

if __name__ == "__main__":
    load_data()
    app.run(debug=True, extra_files=scene_files)
