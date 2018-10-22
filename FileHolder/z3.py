from flask import Flask
from flask import session
from flask import request
from flask import render_template
import os
from os.path import expanduser
from werkzeug import generate_password_hash, check_password_hash
from flask import redirect

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
        

@app.route('/sawickij/z3/userHome')
def userHome():
    if session.get('user'):
      return render_template('userHome.html')
       

@app.route('/sawickij/z3/upload', methods=['POST'])
def upload():
    print(request.files)
    return "OK"

@app.route('/sawickij/z3/logout')
def logout():
    session.pop('user', None)
    return redirect('/sawickij/z3')
