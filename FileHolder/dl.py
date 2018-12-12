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

jwt_secret_key = 'amdsnaiSDSFD2938hxn6vbbzx'

r = redis.Redis()

@app.route('/sawickij/dl/upload', methods=['POST'])
def upload():
    token = request.form['token']
    if tokenVerified(token):
      user_id = secure_filename(getUserFromToken(token))
      userpath = 'storage/' + secure_filename(user_id) + '/'
      userfiles = listUserFiles(user_id)
      f = request.files['uploadedFile']
      if len(userfiles) < 5:
        f.save(userpath + secure_filename(f.filename))
        return redirect('/sawickij/z3/userHome')
      else:
        return redirect('/sawickij/z3/userHome')
    else:
      return redirect('/sawickij/z3/logout')


@app.route('/sawickij/dl/storage/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    token = request.form['token']
    if tokenVerified(token):
      return send_from_directory(directory='storage', filename=filename, as_attachment=True)
    else:
      return redirect('/sawickij/z3/logout')

@app.route('/sawickij/dl/storage/<string:share_token>', methods=['GET', 'POST'])
def shareDownload(share_token):
    share_token_parts =  decodeShareToken(share_token)
    user_id = secure_filename(share_token_parts['user_id'])
    filename = share_token_parts['filename']
    sharePath = user_id + '/' + filename

    return send_from_directory(directory='storage', filename=sharePath, as_attachment=True)


def decodeShareToken(share_token):
  share_token_parts = {}
  share_token_parts = jwt.decode(share_token, jwt_secret_key)
  return share_token_parts

def tokenVerified(token):
  token_parts = {}
  try:
    token_parts = jwt.decode(token, jwt_secret_key)
  except jwt.ExpiredSignatureError:
    return False
  return token_parts['user_id'] == str(r.hget('sawickij:webapp:' + token_parts['sid'], 'user_id'))[2:-1]

def getUserFromToken(token):
  token_parts = {}
  try:
    token_parts = jwt.decode(token, jwt_secret_key)
  except jwt.ExpiredSignatureError:
    return False
  return token_parts['user_id']

def listUserFiles(user_id):
  userpath = 'storage/' + user_id + '/'
  return os.listdir(userpath)
