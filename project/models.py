# project/models.py

import os
import sys
import datetime
import copy
from project import db, bcrypt


class User(db.Model):

	__tablename__ = "users"

	id 				= db.Column(db.Integer, primary_key=True, autoincrement=True)
	email 			= db.Column(db.String(255), unique=True, nullable=False)
	language 		= db.Column(db.String(255), nullable=False)
	password 		= db.Column(db.String(255), nullable=False)
	registered_on 	= db.Column(db.DateTime, nullable=False)
	admin 			= db.Column(db.Boolean, nullable=False, default=False)

	def __init__(self, email, password, language, admin=False):
		self.email 			= email
		self.password 		= bcrypt.generate_password_hash(password)
		self.registered_on 	= datetime.datetime.now()
		self.admin 			= admin
		self.language 		= language

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

	id 					= db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender_email 		= db.Column(db.String(255), nullable=False)
	receiver_email 		= db.Column(db.String(255), nullable=False)
	sender_lan 			= db.Column(db.Integer, nullable=False)
	receiver_lan 		= db.Column(db.Integer, nullable=False)
	message 			= db.Column(db.String(255), unique=True, nullable=False)
	created_date 		= db.Column(db.DateTime, nullable=False)
	date_str   			= db.Column(db.String(255), nullable=False)


	def __init__(self, sender_email, receiver_email, sender_lan, receiver_lan, suffix='.txt'):
		self.sender_email 		= sender_email
		self.receiver_email 	= receiver_email
		self.sender_lan 		= sender_lan
		self.receiver_lan 		= receiver_lan
		self.created_date 		= datetime.datetime.now()
		self.date_str 			= self.created_date.strftime("%Y_%m_%d_%H_%M_%S")
		if not os.path.isdir("./messages_db"): os.mkdir("./messages_db")
		message_loc = "./messages_db/" + "msg_" + self.date_str + "_" + sender_email + "_" + receiver_email + "_orig" + suffix
		self.message 			= message_loc

	def is_text(self):
		return True if ".txt" in self.message else False

	def is_audio(self):
		return True if ".wav" in self.message else False

	def is_video(self):
		return True if ".webm" in self.message else False

	def get_orig_file_name(self):
		return self.message

	def get_trans_file_name(self):
		# !@#_&&&
		fixed_sender_lan = self.sender_lan
		if self.is_audio() or self.is_video():
			fixed_sender_lan = 'en'
		# end-tab
		msg = copy.deepcopy(self.message)
		new_msg = msg.replace("_orig", "_" + fixed_sender_lan + "_to_" + self.receiver_lan)
		return new_msg

	def get_sender_email(self):
		return self.sender_email

	def get_receiver_email(self):
		return self.receiver_email

	def get_sender_language(self):
		return self.sender_lan

	def get_receiver_language(self):
		return self.receiver_lan

	def get_id(self):
		return self.id

	def get_datetime_str(self):
		return self.date_str

	def __repr__(self):
		return '<Msg {0}>'.format(self.message)