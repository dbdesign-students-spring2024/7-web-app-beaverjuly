#!/usr/bin/env python3

import os
import sys
import subprocess
import datetime
import uuid

from flask import Flask, render_template, request, redirect, url_for, make_response, flash

# import logging
import sentry_sdk
from sentry_sdk.integrations.flask import (
    FlaskIntegration,
)  # delete this if not using sentry.io

# from markupsafe import escape
import pymongo
from pymongo.errors import ConnectionFailure
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import session

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
load_dotenv(override=True)  # take environment variables from .env.

# initialize Sentry for help debugging... this requires an account on sentrio.io
# you will need to set the SENTRY_DSN environment variable to the value provided by Sentry
# delete this if not using sentry.io
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # enable_tracing=True,
    # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    integrations=[FlaskIntegration()],
    send_default_pii=True,
)

# instantiate the app using sentry for debugging
app = Flask(__name__)
app.secret_key = 'my_mini_sphere' 
# # turn on debugging if in development mode
# app.debug = True if os.getenv("FLASK_ENV", "development") == "development" else False

# try to connect to the database, and quit if it doesn't work
try:
    cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
    db = cxn[os.getenv("MONGO_DBNAME")]  # store a reference to the selected database

    # verify the connection works by pinging the database
    cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
    print(" * Connected to MongoDB!")  # if we get here, the connection worked!
except ConnectionFailure as e:
    # catch any database errors
    # the ping command failed, so the connection is not available.
    print(" * MongoDB connection error:", e)  # debug
    sentry_sdk.capture_exception(e)  # send the error to sentry.io. delete if not using
    sys.exit(1)  # this is a catastrophic error, so no reason to continue to live


# set up the routes

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'name_myself':
            username = request.form.get('username', '').strip()
            if not username:  # Check if username is empty
                flash('Please give yourself a name.')
                return redirect(url_for('login'))
        elif action == 'be_nameless':
            username = 'Nameless-' + str(uuid.uuid4())[:8]
        else:
            flash('Invalid login attempt.')
            return redirect(url_for('login'))
        
        session['username'] = username
        user = db.users.find_one({"username": username})
        if not user:
            # Create a new user in the database if it does not exist
            db.users.insert_one({"username": username, "bio": ""})
        
        return redirect(url_for('profile'))

    return render_template('login.html')



@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None) 
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    username = session.get('username')
    user = db.users.find_one({"username": username})
    return render_template('profile.html', user=user)

@app.route('/user/<username>')
def read_profile(username):
    user = db.users.find_one({"username": username})
    if not user:
        # Include the username in the flash message
        flash(f"Oops, {username} has gone missing!")
        return redirect(url_for('read'))
    return render_template('read_profile.html', user=user)



@app.route('/update_bio', methods=['POST'])
def update_bio():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    new_bio = request.form['bio']
    db.users.update_one({"username": session['username']}, {"$set": {"bio": new_bio}})
    
    return redirect(url_for('profile'))


@app.route('/delete_bio', methods=['POST'])
def delete_bio():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    #Set bio to an empty string
    db.users.update_one({"username": session['username']}, {"$set": {"bio": ""}})
    
    return redirect(url_for('profile'))




@app.route("/read")
def read():
    """
    Route for GET requests to the read page.
    Displays some information for the user with links to other pages.
    """
    docs = db.exampleapp.find({}).sort(
        "created_at", -1
    )  # sort in descending order of created_at timestamp
    return render_template("read.html", docs=docs)  # render the read template


@app.route("/create", methods=["GET", "POST"])
def create():
    # Check if a user is logged in
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        # Process the submitted form data if the user is logged in
        name = request.form["fname"]
        message = request.form["fmessage"]
        doc = {"name": name, "message": message, "created_at": datetime.datetime.utcnow()}
        db.exampleapp.insert_one(doc)
        return redirect(url_for("read"))  # Redirect after POST
    else:
        # For a GET request, display the form only if the user is logged in
        return render_template("create.html")





@app.route("/edit/<mongoid>")
def edit(mongoid):
    """
    Route for GET requests to the edit page.
    Only the user who created the record can view the form to edit it.
    """
    doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
    return render_template("edit.html", mongoid=mongoid, doc=doc)


@app.route("/edit/<mongoid>", methods=["POST"])
def edit_post(mongoid):
    """
    Route for POST requests to the edit page.
    Only the user who created the record can update it.
    """
    doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
    name = session['username']  
    message = request.form["fmessage"]

    updated_doc = {
        "name": name,
        "message": message,
        "created_at": datetime.datetime.utcnow(),
    }
    db.exampleapp.update_one(
        {"_id": ObjectId(mongoid)}, {"$set": updated_doc}  # match criteria
    )
    return redirect(url_for("read"))



@app.route("/delete/<mongoid>")
def delete(mongoid):
    """
    Route for GET requests to the delete page.
    Only the user who created the record can delete it.
    """
    doc = db.exampleapp.find_one({"_id": ObjectId(mongoid)})
    db.exampleapp.delete_one({"_id": ObjectId(mongoid)})
    return redirect(url_for("read"))



@app.route("/webhook", methods=["POST"])
def webhook():
    """
    GitHub can be configured such that each time a push is made to a repository, GitHub will make a request to a particular web URL... this is called a webhook.
    This function is set up such that if the /webhook route is requested, Python will execute a git pull command from the command line to update this app's codebase.
    You will need to configure your own repository to have a webhook that requests this route in GitHub's settings.
    Note that this webhook does do any verification that the request is coming from GitHub... this should be added in a production environment.
    """
    # run a git pull command
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    pull_output = process.communicate()[0]
    # pull_output = str(pull_output).strip() # remove whitespace
    process = subprocess.Popen(["chmod", "a+x", "flask.cgi"], stdout=subprocess.PIPE)
    chmod_output = process.communicate()[0]
    # send a success response
    response = make_response(f"output: {pull_output}", 200)
    response.mimetype = "text/plain"
    return response


@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template("error.html", error=e)  # render the edit template


# run the app
if __name__ == "__main__":
    # logging.basicConfig(filename="./flask_error.log", level=logging.DEBUG)
    app.run(load_dotenv=True)
