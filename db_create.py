import sqlite3


db = sqlite3.connect("app.db")
c = db.cursor

# create a table of users
command = "CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT,  password TEXT );"
db.execute( command )

command = "CREATE TABLE stories (story_id INTEGER PRIMARY KEY, title TEXT, body TEXT, completed INTEGER );"
db.execute( command )

command = "CREATE TABLE contributions (user_id INTEGER, story_id INTEGER,  edit_stamp TEXT, edit TEXT );"
db.execute( command )

db.commit()
db.close()
