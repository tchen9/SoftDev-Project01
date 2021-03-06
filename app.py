from flask import Flask, flash, render_template, request, session, redirect, url_for
import auth
from auth import logged_in
from db_tool import get_stories, add_story, get_story, add_cont, get_story_title, get_username, get_contribution, get_user_contributions, get_story_body, get_story_complete, get_original_contribution, MAX_CONTRIBUTIONS, get_story_contributions
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = "TH15 15 4 53CR3T K3Y"

#returns the JART site description page
@app.route('/')
def index():
    return render_template('index.html', title = 'JART')

#checks username and password for authenticity
@app.route('/login', methods=['POST', 'GET'])
def login():
# uses helper method to see if the user is logged in
    if logged_in():
	# if they are, alerts the user and brings them to their profile
        flash('You are already logged in!')
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        result = auth.login(request.form['username'], request.form['password'])
        if result == 0:
        # if login succeeds and 0 is returned, alerts the user and brings them to their profile
            flash('You have logged in!')
            return redirect(url_for('profile'))
        elif result == 1:
        # if login fails and 1 is returned, alerts the user that their password is wrong and prompts them to try again
            flash('Incorrect password.')
            return redirect(url_for('login'))
        elif result == 2:
		# if login fails and 2 is returned, alerts the user that their username is wrong and prompts them to try again
            flash('This username doesn\'t exist.')
            return redirect(url_for('login'))
# if they are not logged in, alerts the user and brings them to the login page
    else:
        return render_template('login.html', title = 'Login')

#logs the user out and back to the JART page
@app.route('/logout')
def logout():
# checks to make sure the user is logged in
    if logged_in():
    # if they are, then runs the logout function from auth.py and alerts the user to the success of the function
        auth.logout()
        flash('You have been logged out.')
        return redirect(url_for('index'))
# if they are not logged in, alerts the user and brings them to the login page
    flash('You are not logged in!')
    return redirect(url_for('login'))

#creates a new user
@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
# checks to make sure the user is logged in. If they are, alerts the user and brings them to their profile.
    if logged_in():
        flash('You are already logged in!')
        return redirect(url_for('profile'))
    if request.method == 'POST':
# if not, uses input data to create a new account
        result = auth.create(request.form['username'],
                             request.form['password1'],
                             request.form['password2'])
# if succeeds, flash 0
        if result == 0:
            flash('You have created an account!')
            return redirect(url_for('profile'))
        elif result == 1:
            flash('Your passwords do not match.')
            return redirect(url_for('create_user'))
        elif result == 2:
            flash('This username already exists.')
            return redirect(url_for('create_user'))
    else:
        return render_template('create_user.html', title = 'Create')

#Home page for user after logging in
#Can see contributions the user has made
@app.route('/profile')
def profile():
    print session['user_id']
    if logged_in():
# gets all of the info pertaining to the user's stats
# user's name
        nameUser = get_username(session['user_id'])
# their contributions
        conts = get_user_contributions(session['user_id'])
# a count of their total contributions
        num_conts = len(conts)
# stories, which is populated by the stories the user has contributed to in the past, so they can review them
        stories = {}
        for cont in conts:
            story_id = cont
            story = {}
            story['title'] = get_story_title(story_id)
            story['preview'] = get_story_body(story_id)[:200] + '...'
            story['complete'] = get_story_complete(story_id)
            stories[story_id] = story
        return render_template('profile.html', title = 'Profile', name = nameUser, stories = stories, num_conts = num_conts)
# if they are not logged in, alerts the user and brings them to the login page
    else:
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))

#Displays list of recent stories 
@app.route('/stories')
def stories():
# if the user is logged in, gets all of the stories
    if logged_in():
        stories = get_stories()
        parsed_stories = {}
# then parses through, choosing the ones that the user has not contributed to
        for story in stories:
            if not get_contribution( session['user_id'], story ):
                parsed_stories[story] = stories[story]
                orig_cont = get_original_contribution(story)
                if orig_cont:
                    creator = orig_cont['user_id']
                    parsed_stories[story]['creator'] = get_username(creator)
        rand_story_id = None
        if parsed_stories:
            rand_story_id = random.randint(0, len(stories))
            while rand_story_id not in parsed_stories:
                rand_story_id = random.randint(0, len(stories))
        return render_template('stories.html', title = 'Stories', stories = parsed_stories, rand_story_id = rand_story_id)
# if they are not logged in, alerts the user and brings them to the login page
    else:
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))

#form for user to create their own story by typing in title and body
@app.route('/create_story', methods = ['GET', 'POST'])
def create_story():
    if not logged_in():
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))
# gets data from input boxes for creating a story
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
# adds a story using the function below, then alerts the user that they were successful and brings them back to their profile
        story_id = add_story(title)
        add_cont(session['user_id'], story_id, body)
        flash('Story created successfully!')
        return redirect(url_for('profile'))
    else:
        return render_template('create_story.html', title = 'Create a Story')

#displays last contribution and a form to add text
@app.route('/contribute/<int:story_id>', methods = ['GET', 'POST'])
def contribute(story_id = -1):
# if they are not logged in, alerts the user and brings them to the login page
    if not logged_in():
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))
# if they've contributed to this story before, alerts the user and brings them back to the stories page
    if get_contribution( session['user_id'], story_id ):
        flash('You have already contributed to this story.')
        return redirect(url_for('stories'))
# otherwise, accepts the contribution, alerts the user, and brings them back to their profile
    if request.method == 'POST':
        add_cont( session['user_id'], story_id, request.form['body'] )
        flash('You have contributed to "' + get_story_title(story_id) + '"!')
        return redirect(url_for('profile'))
    else:
# this is the page for editing the story
        story = get_story(story_id)
        conts_left = MAX_CONTRIBUTIONS - len(get_story_contributions(story_id))
        return render_template('edit_story.html', title = 'Contribute', story = story, conts_left = conts_left)

#displays last contribution and a form to add text
@app.route('/view_story/<int:story_id>', methods = ['GET', 'POST'])
def view_story(story_id = -1):
# if they are not logged in, alerts the user and brings them to the login page
    if not logged_in():
        flash('You need to log in or create an account.')
        return redirect(url_for('login'))
# shows the story by retrieving its body and title from the database
    else:
        story = get_story_body(story_id)
        title = get_story_title(story_id)
        return render_template('view_story.html', story = story, title = title)
        
        
if __name__ == '__main__':
    app.debug = True
    app.run()
