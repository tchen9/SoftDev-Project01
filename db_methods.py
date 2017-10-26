import sqlite3
from datetime import datetime


# add a user to the users table
def add_user( user_id, username, password ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()
    # do the command
    command = "INSERT INTO users VALUES( %d, %s, %s )" % (user_id, repr(username), repr(password))
    c.execute(command)
    # commit and close the database
    db.commit()
    db.close()


# add a story to the story table
# for now, always make completed = 0
def add_story( story_id, title, body, completed ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()
    # do the command
    command = "INSERT INTO stories VALUES( %d, %s, %s, %d )" % (story_id,repr(title), repr(body), completed)
    c.execute(command)
    # commit and close the database
    db.commit()
    db.close()



# add an edit to the contribution table AND update the story
# NOTE: doesn't currently mark as completed, will do in the future
def add_cont( user_id, story_id, addition ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()
    # do the command

    # get the timestamp for the contribution
    timestamp = str( datetime.now() )
    # making the actual contribution
    command = "INSERT INTO contributions VALUES( %d, %d, %s, %s )" % (user_id, story_id, repr(timestamp), repr(addition) )
    c.execute(command)

    # update the body of the story
    command = "SELECT body FROM stories WHERE stories.story_id = %d" % (story_id) # get the original text
    for row in c.execute(command):
        body = row[0] + "\n\n" + addition # add the new text
    command = "UPDATE stories SET body = \"%s\" WHERE stories.story_id = %d" % ( body, story_id )
    c.execute(command)

    # commit and close the database
    db.commit()
    db.close()



# extremely basic tests
# add_user(0, "john doe", "random")
# add_story(0, "the room", "this is a bad movie", 0)
# add_cont( 0, 0, "I really don't reccomend it.")
