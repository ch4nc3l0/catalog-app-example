from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_oauthlib.client import OAuth
import flask
import os


# App config
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.static_folder = 'static'
db = SQLAlchemy(app)
oauth = OAuth(app)


# Authentication
github = oauth.remote_app(
    'github',
    consumer_key='test',
    consumer_secret='dev',
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)
@app.route('/login')
def login():
    return flask.render_template('index.html')


# Show all catagories
@app.route('/')
@app.route('/catalog')
def catalog():
    return flask.render_template('index.html')


# Add a new catagory to the catalog
@app.route('/catalog/add')
def addCatagory():
    return flask.render_template('index.html')


# Show all items in a catagory
@app.route('/catalog/<catagory>')
def catagories():
    return flask.render_template('index.html')


# Add an item to the catagory
@app.route('/catalog/<catagory>/add')
def addCatagories():
    return flask.render_template('index.html')


# Update the current catagory
@app.route('/catalog/<catagory>/update')
def updateCatagories():
    return flask.render_template('index.html')


# Delete the current catagory
@app.route('/catalog/<catagory>/delete')
def deleteCatagories():
    return flask.render_template('index.html')


# Show item details
@app.route('/catalog/<catagory>/<item>')
def items():
    return flask.render_template('index.html')


# Update item details
@app.route('/catalog/<catagory>/<item>/update')
def updateItems():
    return flask.render_template('index.html')


# Delete item
@app.route('/catalog/<catagory>/<item>/delete')
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
