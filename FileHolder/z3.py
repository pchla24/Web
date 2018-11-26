from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import send_from_directory
from flask import url_for
import os
from os.path import expanduser
from werkzeug import generate_password_hash, check_password_hash
from flask import redirect
from werkzeug.utils import secure_filename
import redis
import jwt
import uuid
import datetime

app = Flask(__name__)

app.config.from_pyfile('sec.cfg')
#app.config['SESSION_COOKIE_SECURE'] = True

jwt_secret_key = 'amdsnaiSDSFD2938hxn6vbbzx'

r = redis.Redis()

@app.route('/sawickij/z3/')
def index():
    return render_template('index.html')

@app.route('/sawickij/z3/index.html')
def home():
    return render_template('index.html')

@app.route('/sawickij/z3/register')
def register():
    return render_template('register.html')

@app.route('/sawickij/z3/login')
def login():
    return render_template('login.html')

@app.route('/sawickij/z3/signUp', methods=['POST'])
def signUp():
    home = expanduser('~')

    _login = request.form['Login']
    _email = request.form['email']
    _password = request.form['password']

    _hashed_password = generate_password_hash(_password)

    storage_path = home + '/z3/storage/' + _login

    stringToDB ='\n' + _login + ' ' + _email + ' ' + _hashed_password
    database = open('database', 'a')
    database.write(stringToDB)

    if not os.path.exists(storage_path):
      os.makedirs(storage_path)
    
    return redirect('/sawickij/z3/userCreated')

@app.route('/sawickij/z3/userCreated')
def userCreated():
    return render_template('userCreated.html')

@app.route('/sawickij/z3/signIn', methods=['POST'])
def signIn():
    _login = request.form['Login']
    _password = request.form['password']

    if userValidated(_login, _password):
      session['user'] = _login
      sid = str(uuid.uuid4())

      token_elems = {
			  'login': _login,
			  'sid': sid,
			  'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
		  }
      token = str(jwt.encode(token_elems,jwt_secret_key))[2:-1]
      r.hset('sawickij:webapp:'+sid, 'login', _login)
      session['sid'] = sid
      session['token'] = token

        
      return redirect('/sawickij/z3/userHome')

    return redirect('/sawickij/z3/login')
    

@app.route('/sawickij/z3/userHome')
def userHome():
    if session.get('user'):
      username = session['user']
      token = session['token']
      userpath = '/sawickij/dl/storage/' + username + '/'
      userfiles = listUserFiles(username)

      paths = []
      filenames = []

      if len(userfiles) == 0:
        pass
      if len(userfiles) >= 1:
        path1 = userpath + userfiles[0]
        paths.append(path1)
        filenames.append(userfiles[0])
      if len(userfiles) >= 2:
        path2 = userpath + userfiles[1]
        paths.append(path2)
        filenames.append(userfiles[1])
      if len(userfiles) >= 3:
        path3 = userpath + userfiles[2]
        paths.append(path3)
        filenames.append(userfiles[2])
      if len(userfiles) >= 4:
        path4 = userpath + userfiles[3]
        paths.append(path4)
        filenames.append(userfiles[3])
      if len(userfiles) >= 5:
        path5 = userpath + userfiles[4]
        paths.append(path5)
        filenames.append(userfiles[4])

      return render_template('userHome.html', user=username, paths_filenames=zip(paths, filenames), token=token)

    else:
      return redirect('/sawickij/z3/')

@app.route('/sawickij/z3/shareToken', methods=['POST'])
def shareToken():
    _filename = request.form['filename']
    _username = session['user']

    share_token_elems = {
			  'username': _username,
			  'filename': _filename
		}
    share_token = str(jwt.encode(share_token_elems,jwt_secret_key))[2:-1]
    share_link = 'pi.iem.pw.edu.pl/sawickij/dl/storage/' + share_token

    return render_template('shareToken.html', share_link=share_link)


@app.route('/sawickij/z3/logout')
def logout():
    userToLogout = session['user']
    sidToLogout = session['sid']
    r.delete('sawickij:webapp:' + sidToLogout)
    session.pop('user', None)
    session.pop('sid', None)
    session.pop('token', None)
    return redirect('/sawickij/z3')

def listUserFiles(username):
    userpath = 'storage/' + username + '/'
    return os.listdir(userpath)

def userValidated(login, password):
  realPassword = str(r.hget('sawickij:webapp:users', login))[2:-1]
  return check_password_hash(realPassword, password)






