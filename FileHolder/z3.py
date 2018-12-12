from flask import Flask
from flask import session
from flask import request
from flask import Response
from flask import render_template
from flask import send_from_directory
from flask import url_for
from flask import jsonify
import os
from os import environ as env
from os.path import expanduser
from werkzeug import generate_password_hash, check_password_hash
from flask import redirect
from werkzeug.utils import secure_filename
import redis
import jwt
import uuid
import datetime
from authlib.flask.client import OAuth
from functools import wraps
from six.moves.urllib.parse import urlencode
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.from_pyfile('sec.cfg')
app.config['SESSION_COOKIE_SECURE'] = True

client_sec = open('auth0.cfg', 'rb').read().decode('utf-8')

jwt_secret_key = 'amdsnaiSDSFD2938hxn6vbbzx'

r = redis.Redis()

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='Hs-zV6u-ObVbO0on-J5A1MaQp7zGFW9p',
    client_secret=client_sec,
    api_base_url='https://sawickij.eu.auth0.com',
    access_token_url='https://sawickij.eu.auth0.com/oauth/token',
    authorize_url='https://sawickij.eu.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
      if 'profile' not in session:
       # Redirect to Login page here
        return redirect('/sawickij/z3/login')
      return f(*args, **kwargs)

    return decorated


@app.route('/sawickij/z3/callback')
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
  
    sid = str(uuid.uuid4())

    token_elems = {
			  'user_id': session['profile']['user_id'],
			  'sid': sid,
			  'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
		}

    token = str(jwt.encode(token_elems,jwt_secret_key))[2:-1]
    r.hset('sawickij:webapp:'+sid, 'user_id', session['profile']['user_id'])
    session['sid'] = sid
    session['token'] = token

    return redirect('/sawickij/z3/userHome')


@app.route('/sawickij/z3/goToAuth')
def goToAuth():
    return auth0.authorize_redirect(redirect_uri='https://pi.iem.pw.edu.pl/sawickij/z3/callback', audience='https://sawickij.eu.auth0.com/userinfo')



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


"""
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
"""

@app.route('/sawickij/z3/userHome')
@requires_auth
def userHome():
    user_id = secure_filename(session['profile']['user_id'])
    username = session['profile']['name']
    token = session['token']
    userpath = '/sawickij/dl/storage/' + user_id + '/'
    userfiles = listUserFiles(user_id)

    paths = []
      
    for userfile in userfiles:
        path = userpath + userfile
        paths.append(path)
      
    return render_template('userHome.html', user=username, paths_filenames=zip(paths, userfiles), token=token)


@app.route('/sawickij/z3/shareToken', methods=['POST'])
def shareToken():
    _filename = request.form['filename']

    share_token_elems = {
			  'user_id': session['profile']['user_id'],
			  'filename': _filename
		}
    share_token = str(jwt.encode(share_token_elems,jwt_secret_key))[2:-1]
    share_link = 'https://pi.iem.pw.edu.pl/sawickij/dl/storage/' + share_token

    return render_template('shareToken.html', share_link=share_link)


@app.route('/sawickij/z3/logout')
def logout():
    sidToLogout = session['sid']
    r.delete('sawickij:webapp:' + sidToLogout)
    session.clear()
    params = {'returnTo': url_for('index', _external=True), 'client_id': 'Hs-zV6u-ObVbO0on-J5A1MaQp7zGFW9p'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))



def listUserFiles(user_id):
    userpath = 'storage/' + user_id + '/'
    return os.listdir(userpath)

"""
def userValidated(login, password):
  realPassword = str(r.hget('sawickij:webapp:users', login))[2:-1]
  return check_password_hash(realPassword, password)
"""





