# project/__init__.py

import os, glob

from flask import Flask, session, request, render_template
# from flask_session import Session 
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from project.config import BaseConfig
from werkzeug.utils import secure_filename
from flask import jsonify

from project.be_messages import message_db

from project.bridge import Bridge
from deep_translator import GoogleTranslator
import librosa
import soundfile as sf
br = Bridge()

## FIX THIS
asr_model = "./translate/pretrained_models/asr_deepspeech/deepspeech-0.9.3-models.pbmm"
asr_scorer = "./translate/pretrained_models/asr_deepspeech/deepspeech-0.9.3-models.scorer"

# config

app = Flask(__name__)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'super secret key'

msgs = message_db()

app.config.from_object(BaseConfig)


from project.models import User


# routes

def audio_translate(input_audio, output_audio, input_lang, output_lang):

    global asr_model, br
    print(input_audio)
    x,_ = librosa.load(input_audio, sr=16000)
    sf.write(input_audio, x, 16000)
    text_from_speech = br.asr_deepspeech(model=asr_model, scorer=asr_scorer, audio=input_audio)
    print("Transrciption: ", text_from_speech)

    text_translated = br.translate(text_from_speech, input_lang, output_lang)
    print("text translated", text_translated)

    br.txt_to_sp(out_file=output_audio, text=text_translated,lang=output_lang)

@app.route('/')
def index():
    global msgs
    return app.send_static_file('index.html')

@app.route('/upload')
def upload_file():
    global msgs
    return render_template('upload.html')

@app.route('/save_msgs')
def save_msgs():
    global msgs 
    msgs.store_to_file()
    return "STORED IT!"


@app.route('/show_users')
def show_users():
    global msgs 
    users = User.query.all()
    all_msgs = msgs.get_all()
    return str([ user.email for user in users ]) + '<br>' + str(all_msgs)

@app.route('/email')
def get_email():
    global msgs
    if session.get('logged_in'):
        return session.get('user_email')
    else:
        return "no one logged in!"

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
    global msgs
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


@app.route('/api/register', methods=['POST'])
def register():
    global msgs
    json_data = request.json
    user = User(
        email=json_data['email'],
        password=json_data['password'],
        language=json_data['language']
    )
    try:
        db.session.add(user)
        db.session.commit()
        msgs.add_user(user.id)
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/login', methods=['POST'])
def login():
    global msgs
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        session['user_email'] = user.email 
        status = True
    else:
        status = False
    return jsonify({'result': status})


@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_email', None)
    return jsonify({'result': 'success'})


@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})

@app.route('/user_redirect', methods=['GET'])
def user_board():
    global msgs
    if session.get('logged_in'):
        email = session.get('user_email')
        user = User.query.filter_by(email=email).first()

        # return str(user.id)
        incoming_msgs = msgs.get_user_incoming(int(user.id))
        outgoing_msgs = msgs.get_user_outgoing(int(user.id))

        all_msgs = list()
        print("incoming_msgs", incoming_msgs)
        print("outgoing_msgs", outgoing_msgs)


        for msg in incoming_msgs:
            print("msg", msg)

            message = GoogleTranslator(source=sender_language, target=reciever_language).translate(message) 
            all_msgs += [ tuple([ "RECIEVED: ", sender_name, sender_language, message_type, message ]) ]
        # end-tab
        for msg in outgoing_msgs:


            (sender_id, reciever_id, sender_loc, reciever_loc, message_type, message) = msg

            sender = User.query.filter_by(id=sender_id).first()
            sender_name = sender.email 
            sender_language = sender.language

            reciever = User.query.filter_by(id=reciever_id).first()
            reciever_name = reciever.email 
            reciever_language = reciever.language
            print("sender_language", sender_language)
            reciever_name = email 
            message_translated = GoogleTranslator(source=sender_language, target=reciever_language).translate(message) 
            all_msgs += [ tuple([ "SENT: ", sender_name, sender_language, message_type, message ]) ]
            all_msgs += [ tuple([ "SENT: ", sender_name, reciever_language, message_type, message_translated]) ]
        # en
        print(all_msgs)

        messages = glob.glob("/home/sooos/bothhand_v2/project/static/messages/*")
        print("messages", messages)
        for message in messages:

            path = "messages/" + os.path.basename(message)
            print(path)
            if path.split(".")[-1] == "wav":
                                
                message_type = "audio"
                message_translated = message.split(".")[0] + "_translated.wav"
                path_translated = "messages/" + os.path.basename(message).split(".")[0] + "_translated.wav"
                print(path)
                print("path_trans", path_translated)
                print("message trans", message_translated)

                audio_translate(message, message_translated,"en","de")

                all_msgs += [tuple([ "SENT:     ", "Pogba", "en", message_type, path ])]
                all_msgs += [tuple([ "SENT:     ", "Pogba", "de", message_type, path_translated ])]            
            if path.split(".")[-1] == "webm":
#                all_msgs += [tuple([ "SENT:     ", "Pogba", "de", message_type, path ])]
                message_type = "video"
                all_msgs += [tuple([ "SENT:     ", "Pogba", "de", message_type, path ])]
#            print("I am in ")
#            all_msgs += [tuple([ "SENT:     ", "Pogba", "de", message_type, path ])]
#            all_msgs += [tuple([ "SENT:     ", "Pogba", "de", message_type, path_translated ])]            


        return render_template('message_board.html', messages=all_msgs, user_name=user.email)
        # return "Your message board " + str(user.id) +  ": " + "<br>Incoming: " + str(incoming_msgs) + "<br>Outgoing: " + str(outgoing_msgs)
        # return render_template('upload.html')
    # end-tab
    else: 
        return "Not Logged In"
    # end-tab

@app.route('/send_to/message/<receiver_name>', methods=['POST'])
def send_to(receiver_name):
    global msgs 

    json_data = request.json
    msg = json_data["message"]
    msg_type = json_data['message_type']

    reciever = User.query.filter_by(email=receiver_name).first()
    reciever_language = reciever.language
    reciever_id = reciever.id 

    sender_name = session.get('user_email')
    sender = User.query.filter_by(email=sender_name).first()
    sender_id = sender.id
    sender_language = sender.language

    msg_id = msgs.add_msg(sender_id, reciever_id, sender_language, reciever_language, msg_type, msg)


    

@app.route('/new_message', methods=['POST'])
def new_message():
    global msgs

    message = request.form['message']
    msg_type = request.form['message_type']
    receiver_name = request.form['reciever_name']

    print(message, msg_type, receiver_name)

    reciever = User.query.filter_by(email=receiver_name).first()
    reciever_language = reciever.language
    reciever_id = reciever.id 

    sender_name = session.get('user_email')
    sender = User.query.filter_by(email=sender_name).first()
    sender_id = sender.id
    sender_language = sender.language

    msgs.add_msg(sender_id, reciever_id, sender_language, reciever_language, msg_type, message)

    return "message sent"

@app.route('/user_redirect2', methods=['GET'])
def user_redirect():
    global msgs
    if session.get('logged_in'):
        user_email = session.get('user_email')
        user = User.query.filter_by(email=user_email).first()
        print(user_email)
        print(user)

        incoming_msgs = msgs.get_user_incoming(int(user.id))
        outgoing_msgs = msgs.get_user_outgoing(int(user.id))
        # incoming_msgs = msgs.get_all_incoming()
        # outgoing_msgs = msgs.get_all_outgoing()
        all_messages = incoming_msgs + outgoing_msgs 
        test_messages = [ ('text', 'these messages are to test'), ('text', 'test2'), ('text', 'test3') ]
        test_messages.append(('audio', 'messages/sample.mp3'))
        test_messages.append(('audio', 'messages/sample.mp3'))
        test_messages.append(('video', 'messages/sample.mp4'))
        return render_template('message_board.html', messages=test_messages, user_name=user.email)
    else: 
        return "Not Logged In"
    # end-tab



@app.route('/user/messages', methods=['GET'])
def user_board_messages(email, text):
    global msgs
    
    user = User.query.filter_by(email=email).first()
    text = text
    print(text)
    return "got it"
    '''
    if session.get('logged_in') and session.get('user_email') == user.email:
        # return str(user.id)
        incoming_msgs = msgs.get_user_incoming(int(user.id))
        outgoing_msgs = msgs.get_user_outgoing(int(user.id))
        # incoming_msgs = msgs.get_all_incoming()
        # outgoing_msgs = msgs.get_all_outgoing()

        test_messages = [ 'these messages are to test', 'test2', 'test3' ]
        return render_template('message_board.html', messages=test_messages, user_name=user.email)
        # return "Your message board " + str(user.id) +  ": " + "<br>Incoming: " + str(incoming_msgs) + "<br>Outgoing: " + str(outgoing_msgs)
        # return render_template('upload.html')
    # end-tab
    else: 
        return "Not Logged In"
    '''
@app.route('/handle_record', methods=['POST'])
def handle_form():
    print(request.files)
#    print("Posted file: {}".format(request.files['file']))
    
    __UPLOADS__ = "/home/sooos/bothhand_v2/project/static/messages/"

    email = session.get('user_email')
    user = User.query.filter_by(email=email).first()
    ### get to whom TODO

    print("I am here")

    pid = str(os.getpid())

    print("I am logged in")
    print(request)
    files = request.files
    print(files)
    print("pid", pid)
    print("user", str(user))
    print("email", email)
    user = email
    reciever = "Fermi"
    if "audio-blob" in files:

        vfile = request.files["audio-blob"]
        print(vfile.filename)
        vfile.save(vfile.filename)
        os.system("mv "+vfile.filename+" "+__UPLOADS__+user+"_"+reciever+"_"+pid+"_record.wav")
#        os.system("python /home/sooos/bothhand/project/translate/bridge.py "+__UPLOADS__+pid+"record.wav es")

    if "video-blob" in files:
        vfile = request.files["video-blob"]
        print(vfile.filename)
        vfile.save(vfile.filename)
        os.system("mv "+vfile.filename+" "+__UPLOADS__+user+"_"+reciever+"_"+pid+"_record.webm")
#        os.system("python /home/sooos/bothhand/project/translate/bridge.py "+__UPLOADS__+pid+"record.webm es")

    return "got it"

    #db command store path to audio, user_id, reciever_id, message_type

