from flask import Flask, flash, render_template, request, session, redirect, url_for
import auth
from auth import logged_in

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

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
        return render_template('login.html')

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
        return render_template('create_user.html')
    
@app.route('/profile')
def profile():
    return "profile"

@app.route('/stories')
def stories():
    return "stories"

@app.route('/create_story')
def create_story():
    title = request.form['title']
    body = request.form['body']
    return render_template("create_story.html")


@app.route('/contribute')
def contribute_story():
    return "contribute to story"

if __name__ == '__main__':
    app.debug = True
    app.run()
