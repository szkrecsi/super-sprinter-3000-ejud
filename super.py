# all the imports
import os
from peewee import *
from connectdatabase import ConnectDatabase
from models import UserStories
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)  # create the application instance
app.config.from_object(__name__)  # load config from this file, super.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'super.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))
app.config.from_envvar('SUPER_SETTINGS', silent = True)


def init_db():
    ConnectDatabase.db.connect()
    ConnectDatabase.db.drop_tables([UserStories], safe = True)
    ConnectDatabase.db.create_tables([UserStories], safe = True)


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'postgre_db'):
        g.postgre_db.close()


@app.route('/')
def home_page():
    return redirect(url_for('show_stories'))


@app.route('/list')
def show_stories():
    title_list = 'Super Sprinter 3000'
    header = 'User Story Manager'
    entries = UserStories.select().order_by(UserStories.id.asc())
    return render_template('list.html', entries = entries, title = title_list, header = header)


@app.route('/story')
def create_story():
    title_add = 'Super Sprinter 3000 - Add new Story'
    header = 'User Story Manager - Add new Story'
    return render_template('form.html', title = title_add, header = header)


@app.route('/add', methods = ['POST'])
def add_story():
    if not session.get('logged_in'):
        abort(401)
    new_story = UserStories.create(story_title = request.form['story_title'],
                                   user_story = request.form['user_story'],
                                   acceptance_criteria = request.form['acceptance_criteria'],
                                   business_value = request.form['business_value'],
                                   estimation = request.form['estimation'],
                                   status = request.form['status'])
    new_story.save()
    flash('New story was successfully added & posted!')
    return redirect(url_for('show_stories'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
    print(app.config['USERNAME'])
    print(app.config['PASSWORD'])
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were successfully logged in!')
            return redirect(url_for('show_stories'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out. Goodbye!')
    return redirect(url_for('show_stories'))



@app.route('/story/<story_id>', methods=['GET', 'POST'])
def edit_story(story_id):
    title_edit = 'Super Sprinter 3000 - Edit Story'
    header ='User Story Manager - Edit Story'
    story = UserStories.select().where(UserStories.id == story_id)
    return render_template('form.html', title = title_edit, header = header, entry = story[0])
 

@app.route('/update/story<story_id>', methods = ['POST'])
def update_story(story_id):
    story = UserStories.update(story_title = request.form['story_title'],
                               user_story = request.form['user_story'],
                               acceptance_criteria = request.form['acceptance_criteria'],
                               business_value = request.form['business_value'],
                               estimation = request.form['estimation'],
                               status = request.form['status']).where(UserStories.id == story_id)
    story.execute()
    flash('User Story was successfully updated & posted!')
    return redirect(url_for('show_stories'))


@app.route('/delete/story<story_id>', methods = ['GET', 'POST'])
def delete_story(story_id):
    if not session.get('logged_in'):
        abort(401)
    story = UserStories.delete().where(UserStories.id == story_id)
    story.execute()
    return redirect(url_for('show_stories'))

if __name__ == '__main__':
    init_db()
    app.run()
