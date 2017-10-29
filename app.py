from flask import Flask, flash, render_template, request, session, redirect, url_for
import auth
from auth import logged_in
from db_tool import get_stories, add_story, get_story, add_cont, get_story_title

app = Flask(__name__)
app.config['SECRET_KEY'] = "TH15 15 4 53CR3T K3Y"

@app.route('/')
def index():
    return render_template('index.html', title = 'JART')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if logged_in():
        flash('You are already logged in!')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        result = auth.login(request.form['username'], request.form['password'])
        if result == 0:
            flash('You have logged in!')
            return redirect(url_for('profile'))
        elif result == 1:
            flash('Incorrect password.')
            return redirect(url_for('login'))
        elif result == 2:
            flash('This username doesn\'t exist.')
            return redirect(url_for('login'))

    else:
        return render_template('login.html', title = 'Login')

@app.route('/logout')
def logout():
    if logged_in():
        auth.logout()
        flash('You have been logged out.')
        return redirect(url_for('index'))
    flash('You are not logged in!')
    return redirect(url_for('login'))
    
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if logged_in():
        flash('You are already logged in!')
        return redirect(url_for('profile'))
    if request.method == 'POST':
        result = auth.create(request.form['username'],
                             request.form['password1'],
                             request.form['password2'])
        if result == 0:
            flash('You have created an account!')
            return redirect(url_for('profile'))
        elif result == 1:
            flash('Your passwords do not match.')
            return redirect(url_for('create_user'))
        elif result == 2:
            flash('This username already exists.')
            return redirect(url_for('create_user'))
    else:
        return render_template('create_user.html', title = 'Create')
    
@app.route('/profile')
def profile():
    if logged_in():
        return render_template('profile.html', title = 'Profile')
    else:
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))

@app.route('/stories')
def stories():
    if logged_in():
        stories = get_stories()
        return render_template('stories.html', title = 'Stories', stories = stories)
    else:
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))

@app.route('/create_story', methods = ['GET', 'POST'])
def create_story():
    if not logged_in():
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        story_id = add_story(title, body)
        add_cont(session['user_id'], story_id, body)
        flash('Story created successfully!')
        return redirect(url_for('profile'))
    else:
        return render_template('create_story.html', title = 'Create a Story')

#displays last contribution and a form to add text
@app.route('/contribute/<int:story_id>', methods = ['GET', 'POST'])
def contribute(story_id = -1):
    if not logged_in():
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))
    if request.method == 'POST':
        add_cont(session['user_id'], story_id, request.form['body'])
        flash('You have contributed to "' + get_story_title(story_id) + '"!')
        return redirect(url_for('profile'))
    else:
        story = get_story(story_id)
        return render_template('edit_story.html', story = story)

        
if __name__ == '__main__':
    app.debug = True
    app.run()
