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

@app.route('/sawickij/dl/upload', methods=['POST'])
def upload():
    token = request.form['token']
    if tokenVerified(token):
      username = getUserFromToken(token)
      userpath = 'storage/' + username + '/'
      userfiles = listUserFiles(username)
      f = request.files['uploadedFile']
      if len(userfiles) < 5:
        f.save(userpath + secure_filename(f.filename))
        return redirect(url_for('userHome', token=token))
      else:
        return redirect(url_for('userHome', token=token))
    else:
      return redirect('/sawickij/z3/logout')


@app.route('/sawickij/dl/storage/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='storage', filename=filename)

def tokenVerified(token):
  token_parts = {}
  try:
    token_parts = jwt.decode(token, jwt_secret_key)
  except jwt.ExpiredSignatureError:
    return False
  return token_parts['login'] == str(r.hget('sawickij:webapp:' + token_parts['sid'], 'login'))[2:-1]

def getUserFromToken(token):
  token_parts = {}
  try:
    token_parts = jwt.decode(token, jwt_secret_key)
  except jwt.ExpiredSignatureError:
    return False
  return token_parts['login']

def listUserFiles(username):
  userpath = 'storage/' + username + '/'
  return os.listdir(userpath)