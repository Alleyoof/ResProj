from flask import Flask, url_for, session, render_template, redirect, request, Markup, flash
from authlib.integrations.flask_client import OAuth
import os
import pandas as pd
from findLocAndRec import searchLocationsRec
from csvMethods import *
from googleplaces import types
#https://github.com/authlib/demo-oauth-client/blob/master/flask-google-login/app.py

app = Flask(__name__, static_folder='staticFiles')
app.secret_key = os.urandom(12)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
googleClientId = ''
googleSecret = ''
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

@app.route('/cityState')
def cityState():
    return render_template('cityState.html')

@app.route('/recCityState', methods = ["GET", "POST"])
def recCityState():
    session['city'] = request.form.get('city')
    session['state'] = request.form.get('state')
    # print(session['city'])
    # print(session['state'])
    return redirect('/home')

@app.route('/home')
def homePage():
    user = session.get('user')
    city = session.get('city')
    state = session.get('state')
    return render_template('homescreen.html', name=user['given_name'], city = city, state = state)

@app.route('/receiveAdd', methods = ["GET", "POST"])
def addToTable():
    print(request.form)
    name = request.form.get('name')
    address = request.form.get('address', 0)
    userID = session.get('user')['email']
    print(userID)
    rating = request.form.get('rating')
    city = session.get('city')
    state = session.get('state')
    val = findAdd(name, address, city, state, userID, rating)
    return redirect('/allReviews')

@app.route('/allReviews', methods = ["GET", "POST"])
def getRev():
    userID = session.get('user')['email']
    city = session.get('city')
    state = session.get('state')
    val = getReviews(userID, city, state)
    if val == -1:
        return redirect('/home')
    revhtml = "<h2>Reviews</h2><table><tr><th>Name</th><th>Address</th><th>Your Rating</th></tr>"
    for v in val:
        revhtml += f'<tr><td>{v[0]}</td><td>{v[1]}</td><td>{v[2]}</td></tr>'
    revhtml += "</table>"
    revMessage = Markup(revhtml)
    flash(revMessage)
    return render_template('myReviews.html')

@app.route('/delReview', methods = ["GET", "POST"])
def delRev():
    print(request.form)
    address = request.form.get('address', 0)
    userID = session.get('user')['email']
    # print(userID)
    city = session.get('city')
    state = session.get('state')
    name = request.form.get('name')
    print(address)
    val = findDel(name, address, city, state, userID)
    return redirect('/allReviews')

@app.route('/generateRec', methods = ["GET", "POST"])
def createRec():
    # print(request.form)
    latitude = float(request.form.get('latitude', 0))
    longitude = float(request.form.get('longitude', 0))
    searchRadius = int(request.form.get('searchRadius', 0))
    category = request.form.get('categories')
    attributes = request.form.getlist('attributes')
    numSug = int(request.form.get('numSug', 0))
    city = session.get('city')
    state = session.get('state')
    # print(category        
    if "Restaurants" == category:
        myCon = types.TYPE_RESTAURANT
    elif "Fashion" == category:
        myCon = types.TYPE_CLOTHING_STORE
    elif "Barbers" == category:
        myCon = types.TYPE_HAIR_CARE
    else:
        myCon = types.TYPE_DOCTOR
    userID = session.get('user')['email']
    # print(category)
    collabVals, contentVals = searchLocationsRec(latitude, longitude, searchRadius,  
    numSug, city, state, userID, collabAttribute=myCon, contentAttributes=attributes)
    collhtml = "<h2>Collaborative result table:</h2><table><tr><th>Name</th><th>Address</th><th>Predicted Rating</th></tr>"
    for v in collabVals:
        collhtml += f'<tr><td>{v[0]}</td><td>{v[1]}</td><td>{v[2]}</td></tr>'
    collhtml += "</table>"
    collMessage = Markup(collhtml)
    flash(collMessage)
    conthtml = "<h2>Content result table:</h2><table><tr><th>Name</th><th>Address</th><th>Stars (Overall Rating of Place)</th><th>Similarity (%)</th></tr>"
    for v in contentVals:
        conthtml += f'<tr><td>{v[0]}</td><td>{v[1]}</td><td>{v[2]}</td><td>{v[3]}</td></tr>'
    conthtml += "</table>"
    contMessage = Markup(conthtml)
    flash(contMessage)
    # print(contentVals)
    # print(collabVals)
    # collabVals, contentVals = searchLocationsRec(latitude, longitude, searchRadius,  
    # numSug, city, state, 'KoY4KGxev8gdg5qQpyDlZA', typeList=myType, contentAttributes=categories)
    return render_template("recResults.html")

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth')
def auth():
    token = oauth.google.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/cityState')

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('city', None)
    session.pop('state', None)
    return redirect('/')
