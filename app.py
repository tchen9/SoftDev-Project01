from flask import Flask, flash, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "hi"

@app.route('/profile')
def profile():
    return "profile"

@app.route('/stories')
def stories():
    return "stories"

@app.route('/createStory')
def createStory():
    return "create story"

@app.route('/contributeStory')
def contributeStory():
    return "contribute to story"
