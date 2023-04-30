"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""


from flask import render_template, request, jsonify, send_file, flash, redirect, url_for, g
import os
import jwt
from app import app, db
import logging
from app.forms import LoginForm, RegisterForm, PostForm
from app.models import User, Post
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
from datetime import datetime, timedelta
from flask_cors import cross_origin
from flask_wtf.csrf import generate_csrf

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/auth/login', methods=['POST'])
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    timestamp = datetime.utcnow()
    payload = {
        "sub": user.id,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=55)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return jsonify({'token': token, 'message': 'User successfully logged in.'}), 200



@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/users/register', methods=['POST'])
def users():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        profile_photo = form.profile_photo.data

        filename = secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        user = User(username, password, firstname, lastname, email, location, biography, filename)
        db.session.add(user)
        db.session.commit()

        message = 'Your account has been created!'
        response = {
            'message': message,
            "firstname": firstname,
            "lastname": lastname,
            "username": username,
            "password": password,
            "email": email,
            "location": location,
            "biography": biography,
            "profile_photo": filename,
            "joined_on": datetime.utcnow(),
        }
        return jsonify(response=response), 201
    else:
        errors = form_errors(form)
        response = {'errors': errors}
        return jsonify(response= response)

@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@requires_auth
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    posts = Post.query.filter_by(user_id=user_id).all()
    posts_list = []
    for post in posts:
        user_posts = {
            'id': post.id,
            'user_id': post.user_id,
            'photo': post.photo,
            'description': post.caption,
            'created_on': post.created_on.strftime('%Y-%m-%d %H:%M:%S')
        }
        posts_list.append(user_posts)

    response = {
        'id': user.id,
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'location': user.location,
        'biography': user.biography,
        'profile_photo': user.profile_photo,
        'joined_on': user.joined_on.strftime('%B, %Y'),
        'posts': posts_list
    }    
    return jsonify(response), 200
    

@app.route('/api/v1/users/<int:user_id>/posts', methods=['POST'])
@requires_auth
def create_post(user_id):
    form = PostForm()

    if form.validate_on_submit():
        post_photo = form.post_photo.data
        caption = form.caption.data

        filename = secure_filename(post_photo.filename)
        post_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        post = Post(caption, filename, user_id)
        db.session.add(post)
        db.session.commit()

        message = 'Successfully created a new post'
        response = {
            'message': message
        }
        return jsonify(response=response), 201
    
    else:
        errors = form_errors(form)
        response = {'errors': errors}
        return jsonify(response= response)

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


