"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
import os
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm
from app.models import User
from werkzeug.security import check_password_hash



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     form = LoginForm()

#     # change this to actually validate the entire form submission
#     # and not just one field
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#         # Get the username and password values from the form.

#         # Using your model, query database for a user based on the username
#         user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
#         # and password submitted. Remember you need to compare the password hash.
#         # You will need to import the appropriate function to do so.
#         # Then store the result of that query to a `user` variable so it can be
#         # passed to the login_user() method below.

#         # Gets user id, load into session
#         if user is not None and check_password_hash(user.password, password):
#             remember_me = False

#             if 'remember_me' in request.form:
#                 remember_me = True

#             # If the user is not blank, meaning if a user was actually found,
#             # then login the user and create the user session.
#             # user should be an instance of your `User` class
#             login_user(user, remember=remember_me)

#             flash('Logged in successfully.', 'success')

#             next_page = request.args.get('next')
#             return redirect(next_page or url_for('home'))
#         else:
#             flash('Username or Password is incorrect.', 'danger')

#     flash_errors(form)
#     return render_template("login.html", form=form)


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404