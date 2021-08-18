""" Messages API Calls """
import os
import json

class message_db:

	def __init__(self):
		if os.path.exists('message_dbs/') and os.path.exists('message_dbs/messages_incoming_db.json'):
			with open('message_dbs/messages_incoming_db.json','r') as stored_messages:
				self.incoming_msgs = json.load(stored_messages)
			with open('message_dbs/messages_outgoing_db.json','r') as stored_messages:
				self.outgoing_msgs = json.load(stored_messages)
			with open('message_dbs/messages_msg_data_db.json','r') as stored_messages:
				self.msg_id_pairs = json.load(stored_messages)
		else:
			self.incoming_msgs  = dict()
			self.outgoing_msgs  = dict()
			self.msg_id_pairs   = dict()
		# end-tab

	def get_all(self):
		return [ self.incoming_msgs, self.outgoing_msgs ]
	def get_all_incoming(self):
		return self.incoming_msgs
	def get_all_outgoing(self):
		return self.outgoing_msgs

	#specific calls
	def get_user_incoming(self, user_id):
		if user_id in self.incoming_msgs.keys():
			return self.incoming_msgs[user_id]
		else:
			return list()
	def get_user_outgoing(self, user_id):
		if user_id in self.outgoing_msgs.keys():
			return self.outgoing_msgs[user_id]
		else:
			return list()

	def add_user(self, user_id):
		self.incoming_msgs[user_id] = list()
		self.outgoing_msgs[user_id] = list()
		return 1

	def add_msg(self, sender_id, reciever_id, sender_language, reciever_language, message_type, message):
		msg_id = len(self.msg_id_pairs.keys())
		reciever_loc = len(self.incoming_msgs[reciever_id])
		sender_loc = len(self.outgoing_msgs[sender_id])

		self.incoming_msgs[reciever_id]   += [ (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message) ]
		self.outgoing_msgs[sender_id]     += [ (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message) ]
		self.msg_id_pairs[msg_id]          = (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message)
		return msg_id

	def rem_msg(self, message_id):

		sender_id, reciever_id, sender_loc, reciever_loc, message_type, message = self.msg_id_pairs(message_id)
		del incoming_msgs[reciever_id][reciever_loc]
		del outgoing_msgs[sender_id][sender_loc]
		msg_id_pairs[message_id] = None
		return 1

	def store_to_file(self):
		cwd = os.getcwd()
		print(cwd)
		if os.path.exists('./message_dbs/'):
			messages_incoming_db = "./message_dbs/messages_incoming_db.json"
			messages_outgoing_db = "./message_dbs/messages_outgoing_db.json"
			messages_msg_data_db = "./message_dbs/messages_msg_data_db.json"
			with open(messages_incoming_db, 'w') as filehandle:
				json.dump(self.incoming_msgs, filehandle)
			with open(messages_outgoing_db, 'w') as filehandle:
				json.dump(self.outgoing_msgs, filehandle)
			with open(messages_msg_data_db, 'w') as filehandle:
				json.dump(self.incoming_msgs, filehandle)
		#   # end-tab
		# end-tab

	def delete_old_backups(self):
		count = 0
		backup_name = "stored_messages" + str(count) + ".json"
		while path.exists(backup_name):
			os.remove(backup_name)
			count = count + 1
	def _delete_old_backups(self, up_to):
		count = 0
		backup_name = "stored_messages" + str(count) + ".json"
		while path.exists(backup_name):
			if count >= up_to:
				break
			os.remove(backup_name)
			count = count + 1
