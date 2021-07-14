""" Messages API Calls """
import os
import json

class message_db:
    "This is where we hold all the messages"

    def __init__(self):
        # We need to change this to EITHER do this fresh init OR load from file system so that our server can continue to work seemlessly on a restart. 
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

    # We need to just define some simple retrieve functions on our object, ideally this means we could even multi-thread this into its own process pid if we wanted and have requests to "msgs" be a call our server makes locally
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

    # Is message a string? I am assuming it is, if it is an array we can remove the [ ] 
    def add_msg(self, sender_id, reciever_id, sender_language, reciever_language, message_type, message):
        #We should move this message into an object that has a unique idetnfier (msgid), so we want some value pair object
        msg_id = len(self.msg_id_pairs.keys())
        reciever_loc = len(self.incoming_msgs[reciever_id])
        sender_loc = len(self.outgoing_msgs[sender_id])

        self.incoming_msgs[reciever_id]   += [ (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message) ]
        self.outgoing_msgs[sender_id]     += [ (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message) ]
        self.msg_id_pairs[msg_id]          = (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message) 
        return msg_id 
    
    
    # I am imagining we want users to be able to remove entries possibly, but either way it is a good idea to write this up even if unused
    # We probably need to switch message to being an object that includes the "message" string but also an enumerated property we can pass around in python. 
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
        #   #
        #

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

#We probably need to start this object in the main class ¯\_(ツ)_/¯