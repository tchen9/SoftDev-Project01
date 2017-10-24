from flask import Flask, flash, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return "hi"

@app.route('/profile')
def profile():
    return "profile"

