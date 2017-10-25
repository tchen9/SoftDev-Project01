from flask import session
import hashlib
import db_methods

# TODO: db_method names are placeholders until functions are written
# TODO: username v ID as parameters

# Attempts to log in a user given their username and password
# Returns 0 for success, 1 for incorrect password, 2 for username does not exist
def login(username, password):
    if username in db_methods.get_users():
        if check_password(username, password):
            session['username'] = username
            return 0
        return 1
    return 2

# Returns whether a user is logged in
def logged_in():
    return session['username'] is not None

# Logs a user out if they are logged in
def logout():
    if logged_in():
        session.pop('username')

# Checks if user's unhashed password is equal to a plaintext string
def check_password(username, password_to_check):
    return db_methods.get_user(username)['password'] == hashlib.sha224(password_to_check).hexdigest()

# Sets the user's password to a hashed version of the input
def set_password(username, new_password):
    return db_methods.set_user_password(hashlib.sha224(new_password).hexdigest())
