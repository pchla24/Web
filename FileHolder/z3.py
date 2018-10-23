from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import send_from_directory
import os
from os.path import expanduser
from werkzeug import generate_password_hash, check_password_hash
from flask import redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'0329727 qwnsubnsb29'

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

    dataFile = open('database', 'r')
    DBcontent = dataFile.readlines()

    for line in DBcontent:
      splitLine = str(line).split(' ')

      if _login == splitLine[0] and check_password_hash(splitLine[2], _password):
        session['user'] = _login
        return redirect('/sawickij/z3/userHome')

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
        filename3 = userfiles[2], filename4 = userfiles[3], filename5 = userfiles[4])

    else:
      return redirect('/sawickij/z3')

       

@app.route('/sawickij/z3/upload', methods=['POST'])
def upload():
    username = session['user']
    userpath = 'storage/' + username + '/'
    userfiles = listUserFiles(username)
    if len(userfiles) < 5:
      for filee in request.files:
        f = request.files[filee]
        f.save(userpath + secure_filename(f.filename))
      return redirect('/sawickij/z3/userHome')


@app.route('/sawickij/z3/storage/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_from_directory(directory='storage', filename=filename)


@app.route('/sawickij/z3/logout')
def logout():
    session.pop('user', None)
    return redirect('/sawickij/z3')

def listUserFiles(username):
    userpath = 'storage/' + username + '/'
    return os.listdir(userpath)



