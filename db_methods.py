import sqlite3

# open the database
db = sqlite3.connect("app.db")
c = db.cursor()


# add a user to the users table
def add_user( user_id, username, password ):
    command = "INSERT INTO users VALUES( %s, %s, %s )"
