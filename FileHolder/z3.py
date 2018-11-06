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
#app.config['SESSION_COOKIE_PATH'] = "/sawickij/z3"
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
        
      return redirect(url_for('userHome', token=token))

    return redirect('/sawickij/z3/login')
    

@app.route('/sawickij/z3/userHome')
def userHome():
    if session.get('user'):
      username = session['user']
      userpath = 'storage/' + username + '/'
      userfiles = listUserFiles(username)

      userfiles += [''] * (5 - len(userfiles))

      path1 = ''
      path2 = ''
      path3 = ''
      path4 = ''
      path5 = ''

      if len(userfiles) == 0:
        pass
      if len(userfiles) >= 1:
        path1 = userpath + userfiles[0]
      if len(userfiles) >= 2:
        path2 = userpath + userfiles[1]
      if len(userfiles) >= 3:
        path3 = userpath + userfiles[2]
      if len(userfiles) >= 4:
        path4 = userpath + userfiles[3]
      if len(userfiles) >= 5:
        path5 = userpath + userfiles[4]
      
      return render_template('userHome.html', user=username, path1 = path1, path2 = path2,
        path3 = path3, path4 = path4, path5 = path5, filename1 = userfiles[0], filename2 = userfiles[1],
        filename3 = userfiles[2], filename4 = userfiles[3], filename5 = userfiles[4], token = request.args.get('token'))

    else:
      return redirect('/sawickij/z3')

       
"""
@app.route('/sawickij/z3/upload', methods=['POST'])
def upload():
    username = session['user']
    userpath = 'storage/' + username + '/'
    userfiles = listUserFiles(username)
    f = request.files['uploadedFile']
    if len(userfiles) < 5:
      f.save(userpath + secure_filename(f.filename))
      return redirect('/sawickij/z3/userHome')
    else:
      return redirect('/sawickij/z3/userHome')


@app.route('/sawickij/z3/storage/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='storage', filename=filename)
"""

@app.route('/sawickij/z3/logout')
def logout():
    userToLogout = session['user']
    sidToLogout = session['sid']
    r.delete('sawickij:webapp:' + sidToLogout)
    session.pop('user', None)
    return redirect('/sawickij/z3')

def listUserFiles(username):
    userpath = 'storage/' + username + '/'
    return os.listdir(userpath)

def userValidated(login, password):
  realPassword = str(r.hget('sawickij:webapp:users', login))[2:-1]
  return check_password_hash(realPassword, password)






