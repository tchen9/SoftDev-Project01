from flask import session
import hashlib
import db_tool

# TODO: db_method names are placeholders until functions are written
# TODO: username v ID as parameters

# Attempts to log in a user given their username and password
# Returns 0 for success, 1 for incorrect password, 2 for username does not exist
def login(username, password):
    if username in db_tool.get_users():
        if check_password(username, password):
            session['username'] = username
            return 0
        return 1
    return 2

# Returns whether a user is logged in
def logged_in():
    try:
        return session['username'] is not None
    except KeyError:
        return False

# Logs a user out if they are logged in
def logout():
    if logged_in():
        session.pop('username')

# Checks if user's unhashed password is equal to a plaintext string
def check_password(username, password_to_check):
    return db_tool.get_user(username)['password'] == hashlib.sha224(password_to_check).hexdigest()

# Sets the user's password to a hashed version of the input
def set_password(username, new_password):
    return db_tool.set_user_password(hashlib.sha224(new_password).hexdigest())

# Attempts to create a user given their username, password, and retyped password
# Returns 0 for success, 1 for unmatching passwords, 2 for username already exists
def create(username, password1, password2):
    if not username in db_tool.get_users():
        if password1 == password2:
            db_tool.add_user(username, password1)
            login(username, password1)
            return 0
        return 1
    return 2
