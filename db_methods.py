import sqlite3

# open the database
db = sqlite3.connect("app.db")
c = db.cursor()


# add a user to the users table
def add_user( user_id, username, password ):
    command = "INSERT INTO users VALUES( %d, %s, %s )" % (user_id, repr(username), repr(password))
    c.execute(command)
    db.commit()


# testing
# add_user(0, "testname", "testpass")

db.commit()
db.close()
