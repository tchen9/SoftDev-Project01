import sqlite3
from datetime import datetime

# open the database
db = sqlite3.connect("app.db")
c = db.cursor()


# add a user to the users table
def add_user( user_id, username, password ):
    command = "INSERT INTO users VALUES( %d, %s, %s )" % (user_id, repr(username), repr(password))
    c.execute(command)
    db.commit()

    
# add a story to the story table
def add_story( story_id, title, body, completed ):
    command = "INSERT INTO stories VALUES( %d, %s, %s, %d )" % (story_id,repr(title), repr(body), completed)
    c.execute(command)
    db.commit()

    
# add an edit to the contribution table AND update the story
# NOTE: doesn't currently mark as completed, will do in the future
def add_cont( user_id, story_id, addition ):
    # get the timestamp for the contribution
    timestamp = str( datetime.now() )
    # making the actual contribution
    command = "INSERT INTO contributions VALUES( %d, %d, %s, %s )" % (user_id, story_id, repr(timestamp), repr(addition) )
    c.execute(command)
    
    # update the body of the story
    command = "SELECT body FROM stories WHERE stories.story_id = contributions.%d" % (story_id)
    body = c.execute(command)[0]
    body = body + "\n\n" + addition
    command = "UPDATE stories SET body = %s WHERE stories.story_id = contridbutions.%d" % ( body, story_id )
    db.commit()


    
# extremely basic tests
add_user(0, "john doe", "random")
add_story(0, "the room", "this is a bad movie.", 0)
add_cont        ( 0, 0, "I really don't reccomend it")

db.commit()
db.close()
