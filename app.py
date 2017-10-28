from flask import Flask, flash, render_template, request, session, redirect, url_for
import auth
from auth import logged_in
from db_tool import get_stories

app = Flask(__name__)
app.config['SECRET_KEY'] = "TH15 15 4 53CR3T K3Y"

@app.route('/')
def index():
    return render_template('index.html', title = 'JART')

@app.route('/login', methods=['GET', 'POST'])
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
    return render_template('profile.html', title = 'Profile')

@app.route('/stories')
def stories():
    stories = get_stories()
    return render_template('stories.html', title = 'Stories', stories = stories)

@app.route('/create_story')
def create_story():
    return render_template('create_story.html', title = 'Create a Story')

@app.route('/contribute')
def contribute():
    return "contribute to story"

if __name__ == '__main__':
    app.debug = True
    app.run()
