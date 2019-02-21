from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user, login_required
from requests_oauthlib import OAuth2Session
import flask
import os


# App config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['SUPER_SECRET_KEY']
app.static_folder = 'static'
db = SQLAlchemy(app)
logMan = LoginManager(app)
logMan.login_view = 'login'


from models import User


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        if 'github' in flask.request.form:
            return flask.redirect('auth')
        elif 'redirect' in flask.request.form:
            return flask.redirect('catalog')
    return flask.render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return flask.render_template('index.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if flask.request.method == 'POST':
        if 'revoke_github' in flask.request.form:
            logout_user
            return flask.redirect('https://github.com/settings/connections/applications/%s'
                                  % os.environ['GIT_CLIENT_ID'])
    user = current_user
    return flask.render_template('profile.html', user=user)


# Github OAuth Links
git_authorization_base_url = 'https://github.com/login/oauth/authorize'
git_token_url = 'https://github.com/login/oauth/access_token'


@app.route('/auth')
def auth():
    # Check if user is already authenticated
    if current_user.is_authenticated:
        # Redirect a user to the page they tried to log in from
        next_page = flask.request.args.get('next')
        if not next_page:
            next_page = flask.url_for('catalog')
        return flask.redirect(next_page)

    # Check if user has an auth token already, if so log user in
    if flask.session.get('oauth_token') is True:
        github = OAuth2Session(os.environ['GIT_CLIENT_ID'],
                               token=flask.session['oauth_token'])
        response = github.get('https://api.github.com/user')
        load_profile = response.json()
        user = User.query.fliter_by(id=load_profile['id']).one()
        login_user(user)

    # Redirect user to github for authentication
    github = OAuth2Session(os.environ['GIT_CLIENT_ID'])
    authorization_url, state = github.authorization_url(
        git_authorization_base_url)
    flask.session['oauth_state'] = state
    return flask.redirect(authorization_url)


@app.route('/callback', methods=["GET"])
def callback():
    # If the user is authorized get token
    github = OAuth2Session(os.environ['GIT_CLIENT_ID'],
                           state=flask.session['oauth_state'])
    token = github.fetch_token(git_token_url,
                               client_secret=os.environ['GIT_CLIENT_SECRET'],
                               authorization_response=flask.request.url)
    flask.session['oauth_token'] = token

    # Use token to load user profile
    github = OAuth2Session(os.environ['GIT_CLIENT_ID'],
                           token=flask.session['oauth_token'])
    response = github.get('https://api.github.com/user')
    load_profile = response.json()

    # Check if the user is already in the database, if so log them in
    if User.query.filter_by(id=load_profile['id']).one() is not None:
        user = User.query.filter_by(id=load_profile['id']).one()
        login_user(user)

    # If user is not in the database make a new entry
    else:
        newUser = User(username=load_profile['login'],
                       id=load_profile['id'],
                       picurl=load_profile['avatar_url'])
        db.session.add(newUser)
        db.session.commit()
        login_user(newUser)

    # Redirect a user to the page they logged in from
    next_page = flask.request.args.get('next')
    if not next_page:
        next_page = flask.url_for('catalog')
    return flask.redirect(next_page)


# Show all catagories
@app.route('/')
@app.route('/catalog')
def catalog():
    return flask.render_template('index.html')


# Add a new catagory to the catalog
@app.route('/catalog/add')
@login_required
def addCatagory():
    return flask.render_template('user.html')


# Show all items in a catagory
@app.route('/catalog/<catagory>')
def catagories():
    return flask.render_template('index.html')


# Add an item to the catagory
@app.route('/catalog/<catagory>/add')
@login_required
def addCatagories():
    return flask.render_template('index.html')


# Update the current catagory
@app.route('/catalog/<catagory>/update')
@login_required
def updateCatagories():
    return flask.render_template('index.html')


# Delete the current catagory
@app.route('/catalog/<catagory>/delete')
@login_required
def deleteCatagories():
    return flask.render_template('index.html')


# Show item details
@app.route('/catalog/<catagory>/<item>')
def items():
    return flask.render_template('index.html')


# Update item details
@app.route('/catalog/<catagory>/<item>/update')
@login_required
def updateItems():
    return flask.render_template('index.html')


# Delete item
@app.route('/catalog/<catagory>/<item>/delete')
@login_required
def deleteItems():
    return flask.render_template('index.html')


# json data for catalog page
@app.route('/catalog/json')
def jsonCatalog():
    return flask.render_template('index.html')


# json data for a catagory page
@app.route('/catalog/<catagory>/json')
def jsonCatagories():
    return flask.render_template('index.html')


# json data for an item
@app.route('/catalog/<catagory>/<item>/json')
def jsonItems():
    return flask.render_template('index.html')
