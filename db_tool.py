import sqlite3
from datetime import datetime

# make the initial database
def make_database():
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create a table of users
    command = "CREATE TABLE users (user_id INTEGER PRIMARY KEY, username TEXT,  password TEXT );"
    db.execute( command )

    # create a table of stories
    command = "CREATE TABLE stories (story_id INTEGER PRIMARY KEY, title TEXT, body TEXT, completed INTEGER );"
    db.execute( command )

    # create a table of contributions
    command = "CREATE TABLE contributions (user_id INTEGER, story_id INTEGER,  timestamp TEXT, edit TEXT );"
    db.execute( command )

    # save changes and close
    db.commit()
    db.close()



# add a user to the users table
def add_user( username, password ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # set the user_id
    command = "SELECT count(*) FROM users;"
    for row in c.execute(command):
        user_id = row[0]

    # do the command
    command = "INSERT INTO users VALUES( %d, \"%s\", \"%s\" );" % (user_id, username, password)
    c.execute(command)

    # commit and close the database
    db.commit()
    db.close()



# add a story to the story table
# for now, always make completed = 0
def add_story( title, body ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # set the story_id
    command = "SELECT count(*) FROM stories;"
    for row in c.execute(command):
        story_id = row[0]

    # do the command
    command = "INSERT INTO stories VALUES( %d, \"%s\", \"%s\", 0 );" % (story_id, title, body )
    c.execute(command)

    # commit and close the database
    db.commit()
    db.close()




# add an edit to the contribution table AND update the story
def add_cont( user_id, story_id, addition ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()
    # do the command

    # get the timestamp for the contribution
    timestamp = str( datetime.now() )

    # making the actual contribution
    command = "INSERT INTO contributions VALUES( %d, %d, \"%s\", \"%s\" );" % (user_id, story_id, timestamp, addition )
    c.execute(command)

    # update the body of the story
    command = "SELECT body FROM stories WHERE stories.story_id = %d;" % (story_id) # get the original text
    for row in c.execute(command):
        body = row[0] + "\n\n" + addition # add the new text
    command = "UPDATE stories SET body = \"%s\" WHERE stories.story_id = %d;" % ( body, story_id )
    c.execute(command)

    # check to see if a story is completed or not
    # get the number of contributions
    command = "SELECT count(*) FROM contributions WHERE contributions.story_id = %d;" % ( story_id )
    for row in c.execute(command):
        count = row[0]
    # if the number of contributions is >= 3, set the status to completed
    if (count >= 3):
        command = "UPDATE stories SET completed = 1 WHERE stories.story_id = %d;" % ( story_id )
        c.execute(command)

    # commit and close the database
    db.commit()
    db.close()


#===========================================================================================================


if __name__ == "__main__":
    # MAKE THE DATABASE:
    make_database()

    # TO INCLUDE ANY DATABASE INFORMATION FOR TESTING PURPOSES:
    # 1. Delete the app.db file
    # 2. Add the command bellow
    # 3. Run the file

    add_user("bob", "pass")
    add_user("jim", "random")
    add_user("unknown", "bird")

    add_story("first story", "First line!")
    add_story("second story", "random text is fun!")

    add_cont(0, 0, "Second line!")
    add_cont(1, 0, "Third line!")
    add_cont(2, 0, "Fourth line!")
