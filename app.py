import sqlite3
import csv

from flask import Flask, flash, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "this is not secure"

@app.route('/')
def home():
    return "hi"
