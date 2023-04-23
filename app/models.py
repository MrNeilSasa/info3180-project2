from datetime import datetime
from . import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    email =  db.Column(db.String(80))
    location = db.Column(db.String(80))
    biography = db.Column(db.String(500))
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)    
    

class Likes(db.Model):
    __tablename__ = "Likes"
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id
    def __repr__(self):
        return '<PostId %r>' % (self.post_id)
    

class Follows(db.Model):
    __tablename__ = "Follows"
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)   


    def __init__(self, follower_id, user_id):
        self.follwer_id = follower_id
        self.user_id = user_id
    def __repr__(self):
        return '<UserId %r>' % (self.follower_id)