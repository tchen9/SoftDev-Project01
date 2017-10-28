from flask import session
import hashlib
import db_tool


# Attempts to log in a user given their username and password
# Returns 0 for success, 1 for incorrect password, 2 for username does not exist
def login(username, password):
    user = db_tool.get_user_by_username(username)
    if user:
        if check_password(user['id'], password):
            session['user_id'] = user['id']
            return 0
        return 1
    return 2

# Returns whether a user is logged in
def logged_in():
    try:
        return session['user_id'] is not None
    except KeyError:
        return False

# Logs a user out if they are logged in
def logout():
    if logged_in():
        session.pop('user_id')

# Checks if user's unhashed password is equal to a plaintext string
def check_password(user_id, password_to_check):
    return db_tool.get_password(user_id) == hashlib.sha224(password_to_check).hexdigest()

# Sets the user's password to a hashed version of the input
def set_password(user_id, new_password):
    db_tool.set_password(user_id, hashlib.sha224(new_password).hexdigest())

# Attempts to create a user given their username, password, and retyped password
# Returns 0 for success, 1 for unmatching passwords, 2 for username already exists
def create(username, password1, password2):
    if not username in db_tool.get_users():
        if password1 == password2:
            user_id = db_tool.add_user(username)
            set_password(user_id, password1)
            login(username, password1)
            return 0
        return 1
    return 2
