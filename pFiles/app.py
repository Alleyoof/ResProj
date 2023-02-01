from flask import Flask, url_for, session, render_template, redirect, request, make_response
from authlib.integrations.flask_client import OAuth
import os
import pandas as pd
from findLocAndRec import searchLocationsRec
from csvMethods import *
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

@app.route('/')
def loginQuery():
    return render_template('loginPage.html')

@app.route('/home')
def homePage():
    user = session.get('user')
    # print(user)
    return render_template('homescreen.html', name=user['given_name'])

@app.route('/receiveAdd', methods = ["GET", "POST"])
def addToTable():
    print(request.form)
    address = request.form.get('address', 0)
    userID = session.get('user')['email']
    print(userID)
    rating = request.form.get('rating')
    city = request.form.get('city')
    state = request.form.get('state')
    val = findAdd(address, city, state, userID, rating)
    if val == -1:
        print('value failed to add')
        # do something to show it broke
    else:
        print('value added')
    return redirect('/home')

@app.route('/allReviews', methods = ["GET", "POST"])
def getRev():
    userID = session.get('user')['email']
    state = request.form.get("state")
    city = request.form.get("city")
    val = getReviews(userID, city, state)
    if val == -1:
        return redirect('/home')
    myStr = "Name | Address | Rating\n"
    for c in val:
        myStr += f'{c[0][1:-1]} | {c[1]} | {c[2]}\n'
    return render_template('myReviews.html', reviews = myStr)

@app.route('/delReview', methods = ["GET", "POST"])
def delRev():
    print(request.form)
    address = request.form.get('address', 0)
    userID = session.get('user')['email']
    print(userID)
    rating = request.form.get('rating')
    city = request.form.get('city')
    state = request.form.get('state')
    val = findDel(address, city, state, userID, rating)
    if val == -1:
        print()
        print('value failed to add')
        print()
    return redirect('/home')

@app.route('/generateRec', methods = ["GET", "POST"])
def createRec():
    latitude = float(request.form.get('latitude', 0))
    longitude = float(request.form.get('longitude', 0))
    searchRadius = int(request.form.get('searchRadius', 0))
    categories = request.form.get('categories', 0).split(",")
    numSug = int(request.form.get('numSug', 0))
    city = request.form.get('city', 0)
    state = request.form.get('state', 0)
    types = request.form.get('types', 0)
    userID = session.get('user')['email']
    # searchLocationsRec(latitude, longitude, searchRadius, categories, 
    # numSug, city, state, userID)
    collabVals, contentVals = searchLocationsRec(latitude, longitude, searchRadius, categories, 
    numSug, city, state, 'G5BqF32PyIQ5IvplDvpKnA')
    myStr = ""
    for c in collabVals:
        myStr += f'{c[0][1:-1]} | {c[1]}\n'
    for c in contentVals:
        myStr += f'{c[0][1:-1]} | {c[1]}\n'
    return render_template("recResults.html", results = myStr)

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
