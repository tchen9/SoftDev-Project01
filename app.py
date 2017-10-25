from flask import Flask, flash, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/profile')
def profile():
    return "profile"

@app.route('/stories')
def stories():
    return "stories"

@app.route('/createStory')
def createStory():
    title = request.form['title']
    body = request.form['body']
    return render_template("create_story.html")

@app.route('/contributeStory')
def contributeStory():
    return "contribute to story"
