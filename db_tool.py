import sqlite3
from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
MAX_CONTRIBUTIONS = 10

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
def add_user( username ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # set the user_id
    command = "SELECT count(*) FROM users;"
    for row in c.execute(command):
        user_id = row[0]

    # do the command
    command = "INSERT INTO users VALUES( %d, \"%s\", \"\" );" % (user_id, username)
    c.execute(command)

    # commit and close the database
    db.commit()
    db.close()

    return user_id


# add a story to the story table
# for now, always make completed = 0
def add_story( title ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # set the story_id
    command = "SELECT count(*) FROM stories;"
    for row in c.execute(command):
        story_id = row[0]

    # do the command
    command = "INSERT INTO stories VALUES( %d, \"%s\", \"%s\", 0 );" % (story_id, title, '' )
    c.execute(command)
    
    # commit and close the database
    db.commit()
    db.close()

    return story_id


# add an edit to the contribution table AND update the story
def add_cont( user_id, story_id, addition ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # get the timestamp for the contribution
    timestamp = datetime.now().strftime(DATETIME_FORMAT)

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
    # if the number of contributions is >= MAX_CONTRIBUTIONS, set the status to completed
    if (count >= MAX_CONTRIBUTIONS):
        command = "UPDATE stories SET completed = 1 WHERE stories.story_id = %d;" % ( story_id )
        c.execute(command)

    # commit and close the database
    db.commit()
    db.close()
    

# returns a dictionary with fields as keys and values as the records for that user_id
def get_user( user_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    user = {}

    # get the user info
    command = "SELECT username, password FROM users WHERE users.user_id = %d;" % (user_id)
    for row in c.execute(command):
        user["username"] = row[0]
        user["password"] = row[1]

    # commit and close the database
    db.commit()
    db.close() 

    return user


# returns a dictionary with fields as keys and values as the records for that user_id
def get_user_by_username( username ):
    
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    user = {}

    # get the user info
    command = "SELECT user_id, password FROM users WHERE users.username = \"%s\";" % (username)
    for row in c.execute(command):
        user["id"] = row[0]
        user["password"] = row[1]

    db.close()
        
    return user


# returns a dictionary with keys as user_ids and values as dictionaries for those users
def get_users():
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    users = {}

    # get the data
    command = "SELECT * FROM users;"
    for row in c.execute(command):
        user = {}
        user[ 'username' ] = row[1]
        user[ 'password' ] = row[2]
        users[ row[0] ] = user

    # commit and close the database
    db.commit()
    db.close()

    return users


# returns a dictionary with keys as story_ids and values as dictionaries for those stories
def get_stories():
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    stories = {}

    # get the data
    command = "SELECT * FROM stories;"
    for row in c.execute(command):
        story = {}
        story[ 'title' ] = row[1]
        story[ 'body' ] = row[2]
        story[ 'complete' ] = row[3]
        stories[ row[0] ] = story

    command = "SELECT * FROM contributions;"
    time = datetime(1,1,1)
    for row in c.execute(command):
        story = stories[ row[1] ]
        cont_time = datetime.strptime(row[2], DATETIME_FORMAT)
        if cont_time > time:
            story['last_contribution'] = row[2]
        
    db.close()

    return stories


def get_user_contributions( user_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    conts = {}

    # get the data
    command = "SELECT * FROM contributions WHERE contributions.user_id = %d;" % (user_id)
    for row in c.execute(command):
        cont = {}
        cont[ 'timestamp' ] = row[2]
        cont[ 'edit' ] = row[3]
        conts[ row[1] ] = cont

    db.close()

    return conts


def get_story_contributions( story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    conts = {}

    # get the data
    command = "SELECT * FROM contributions WHERE contributions.story_id = %d;" % (story_id)
    for row in c.execute(command):
        cont = {}
        cont[ 'timestamp' ] = row[2]
        cont[ 'edit' ] = row[3]
        conts[ row[0] ] = cont

    db.close()

    return conts


def get_contribution( user_id, story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    cont = {}

    # get the data
    command = "SELECT timestamp, edit FROM contributions WHERE contributions.user_id = %d AND contributions.story_id = %d;" % (user_id, story_id)
    for row in c.execute(command):
        cont[ 'timestamp' ] = row[0]
        cont[ 'edit' ] = row[1]
            
    db.close()

    return cont


def get_original_contribution( story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    story = {}
    
    command = "SELECT * FROM contributions WHERE contributions.story_id = %d;" % (story_id)
    first_cont = True
    for row in c.execute(command):
        if first_cont:
            time = datetime.strptime(row[2], DATETIME_FORMAT)
            first_cont = False
        cont_time = datetime.strptime(row[2], DATETIME_FORMAT)
        if cont_time <= time:
            story['user_id'] = row[0]
            story['last_contribution'] = row[2]
            story['edit'] = row[3]

    db.close()
            
    return story
            
# returns the username associated with a given user_id
def get_username( user_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # get the username
    command = "SELECT username FROM users WHERE users.user_id = %d;" % (user_id)
    for row in c.execute( command ):
        name = row[0]

    # commit and close the database
    db.commit()
    db.close()
    return name


# returns the password associated with a given user_id (hashed)
def get_password( user_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # get the username
    command = "SELECT password FROM users WHERE users.user_id = %d;" % (user_id)
    for row in c.execute( command ):
        password = row[0]

    # commit and close the database
    db.commit()
    db.close()
    return password


def get_story( story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # create the dictionary to return
    story = {}

    # get the story info
    command = "SELECT * FROM stories WHERE stories.story_id = %d;" % (story_id)
    for row in c.execute(command):
        story['title'] = row[1]
        story['body'] = row[2]
        story['complete'] = row[3]

    command = "SELECT * FROM contributions WHERE contributions.story_id = %d;" % (story_id)
    time = datetime(1,1,1)
    for row in c.execute(command):
        cont_time = datetime.strptime(row[2], DATETIME_FORMAT)
        if cont_time > time:
            time = cont_time
            story['previous_contribution'] = row[3]

    if time == datetime(1,1,1):
        story['previous_contribution'] = ''
            
    # commit and close the database
    db.commit()
    db.close() 

    return story


# returns the title associated with a given story_id
def get_story_title( story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # get the username
    command = "SELECT title FROM stories WHERE stories.story_id = %d;" % (story_id)
    for row in c.execute( command ):
        title = row[0]

    # commit and close the database
    db.commit()
    db.close()
    return title


# returns the title associated with a given story_id
def get_story_body( story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # get the username
    command = "SELECT body FROM stories WHERE stories.story_id = %d;" % (story_id)
    for row in c.execute( command ):
        body = row[0]

    # commit and close the database
    db.commit()
    db.close()
    return body


# returns the completeness associated with a given story_id
def get_story_complete( story_id ):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()

    # get the username
    command = "SELECT completed FROM stories WHERE stories.story_id = %d;" % (story_id)
    for row in c.execute( command ):
        complete = row[0]

    # commit and close the database
    db.commit()
    db.close()
    return complete


# sets a user's password to the input
def set_password(user_id, password):
    # open the database
    db = sqlite3.connect("app.db")
    c = db.cursor()
    
    command = "UPDATE users SET password = \"%s\" WHERE users.user_id = %d;" % (password, user_id)
    c.execute(command)

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

    jart = add_user('JART')
    set_password(jart, 'autogenerate')
    
    story1 = add_story('Birds')
    add_cont(jart, story1, 'Birds are fascinating creatures.')

    story2 = add_story('Google')
    add_cont(jart, story2, 'Google is a well-known tech company.')

    story3 = add_story('A Day at School')
    add_cont(jart, story3, 'It was an uneventful day at school, when suddenly')

    story4 = add_story('The Prince and the Princess')
    add_cont(jart, story4, 'Once upon a time, there was a princess who lived in a castle.')

    story5 = add_story('???')
    add_cont(jart, story5, 'Darkness descended upon the world.')
    
    '''
    print( "Getting user 0:")
    print( get_user(0) )

    print( "Getting all users:" )
    print( get_users() )

    print( "Getting username for user 1:")
    print( get_username(1) )

    print( "Getting password for user 2:")
    print( get_pass(2) )

    print( "Getting title for story 0:" )
    print( get_story_title(0) )
    print( "Getting body for story 0:" )
    print( get_story_body(0) )
'''
