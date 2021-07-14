# project/models.py


import datetime
from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    language = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, language, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.language = language

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User {0}>'.format(self.email)

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id = db.Column(db.Integer, unique=True, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    sender_loc = db.Column(db.Integer, nullable=False)
    receiver_loc = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(255), unique=True, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)


    def __init__(self, sender_id, receiver_id, sender_loc, receiver_loc, admin=False):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.sender_loc = sender_loc
        self.receiver_loc = receiver_loc
        self.created_date = datetime.datetime.now()
