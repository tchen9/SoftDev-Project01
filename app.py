<<<<<<< HEAD
import sqlite3
import csv

=======
>>>>>>> 846d2b0a08aad64988bc69ec6c3e5c2da61e71aa
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
