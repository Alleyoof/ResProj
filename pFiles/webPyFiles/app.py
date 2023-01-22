from flask import Flask, url_for, session
from flask import render_template, redirect
from authlib.integrations.flask_client import OAuth
import os
import pandas as pd
#https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py

app = Flask(__name__)
app.secret_key = os.urandom(12)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
googleClientId = '998511586381-jir9hao48i7ua4ukmkd3ln8bo4k6n4g8.apps.googleusercontent.com'
googleSecret = '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'
oauth = OAuth(app)

oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id=googleClientId,
    client_secret= googleSecret,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
myCity = 'Mad'
myState = 'Wis'
dfrev = pd.read_csv(f'C:\\Users\\vpjon\\OneDrive\\Documents\\Research Project\\csvFiles\\y{myCity.lower()}_{myState.lower()}.csv',
header=0, 
index_col='review_id',
names=['review_id', 'user_id','business_id', 'stars'])

dfbusi = pd.read_csv(f'C:\\Users\\vpjon\\OneDrive\\Documents\\Research Project\\csvFiles\\b{myCity.lower()}_{myState.lower()}.csv',
header=0, 
index_col = 'business_id',
names = ['business_id','name','neighborhood','address','city','state','postal_code','latitude','longitude','stars','review_count','is_open','categories'])

@app.route('/')
def loginQuery():
    return render_template('loginPage.html')

@app.route('/home')
def homePage():
    user = session.get('user')
    print(user)
    return render_template('homescreen.html', name=user['given_name'])

@app.route('/receive')
def addToTable():
    f = 2

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

