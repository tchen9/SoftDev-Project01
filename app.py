from flask import Flask, flash, render_template, request, session, redirect, url_for
import auth
from auth import logged_in
import db_methods

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    if not logged_in():
        
        result = auth.login()
        if result == 0:
            flash('You have logged in!')
            return redirect(url_for('profile'))
        elif result == 1:
            flash('Incorrect password.')
            return redirect(url_for('login'))
        elif result == 2:
            flash('This username doesn\'t exist.')
            return redirect(url_for('login'))
        
    flash('You are already logged in!')
    return redirect(url_for('index'))
        
@app.route('/profile')
def profile():
    return "profile"

@app.route('/stories')
def stories():
    return "stories"

@app.route('/create_story')
def create_story():
    return render_template("create_story.html")

@app.route('/contribute')
def contribute_story():
    return "contribute to story"

if __name__ == "__main__":
	app.debug = True
app.run()
