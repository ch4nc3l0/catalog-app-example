from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, request, url_for, redirect, render_template, session
from flask_login import LoginManager, current_user
from flask_login import login_user, logout_user, login_required
from flask_marshmallow import Marshmallow
from requests_oauthlib import OAuth2Session
import os


# App config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ['SUPER_SECRET_KEY']
app.static_folder = 'static'
db = SQLAlchemy(app)
ma = Marshmallow(app)
logMan = LoginManager(app)
logMan.login_view = 'login'


from models import User, Category, Item
from models import UserSchema, CategorySchema, ItemSchema
category_schema = CategorySchema(many=True)
item_schema = ItemSchema(many=True)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'github' in request.form:
            return redirect('auth')
        elif 'redirect' in request.form:
            return redirect('catalog')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('catalog')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        if 'revoke_github' in request.form:
            logout_user
            return redirect('https://github.com/settings/connections/applications/%s'
                            % os.environ['GIT_CLIENT_ID'])
    user = current_user
    return render_template('profile.html', user=user)


# Github OAuth Links
git_authorization_base_url = 'https://github.com/login/oauth/authorize'
git_token_url = 'https://github.com/login/oauth/access_token'


@app.route('/auth')
def auth():
    # Check if user is already authenticated
    if current_user.is_authenticated:
        # Redirect a user to the page they logged in from
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('catalog')
        return redirect(next_page)

    # Check if user has an auth token already, if so log user in
    if session.get('oauth_token') is True:
        github = OAuth2Session(os.environ['GIT_CLIENT_ID'],
                               token=session['oauth_token'])
        response = github.get('https://api.github.com/user')
        load_profile = response.json()
        user = User.query.fliter_by(id=load_profile['id']).one()
        login_user(user)

    # Redirect user to github for authentication
    github = OAuth2Session(os.environ['GIT_CLIENT_ID'])
    authorization_url, state = github.authorization_url(
        git_authorization_base_url)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route('/callback', methods=["GET"])
def callback():
    # If the user is authorized get token
    github = OAuth2Session(os.environ['GIT_CLIENT_ID'],
                           state=session['oauth_state'])
    token = github.fetch_token(git_token_url,
                               client_secret=os.environ['GIT_CLIENT_SECRET'],
                               authorization_response=request.url)
    session['oauth_token'] = token

    # Use token to load user profile
    github = OAuth2Session(os.environ['GIT_CLIENT_ID'],
                           token=session['oauth_token'])
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
    next_page = request.args.get('next')
    if not next_page:
        next_page = url_for('catalog')
    return redirect(next_page)


# Show all catagories / most recent items
@app.route('/', methods=['GET', 'POST'])
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    user = ''
    categories = Category.query.all()
    items = Item.query.order_by(Item.timestamp).limit(15).all()
    if current_user.is_authenticated:
        user = current_user
    if request.method == "POST":
        if 'login' in request.form:
            return redirect('login')
        if 'logout' in request.form:
            return redirect('logout')

# --DEVELOPER LOGIN-REMOVE BEFORE LAUNCH-DEVELOPER LOGIN-REMOVE BEFORE LAUNCH--
        if 'dev' in request.form:
            devuser = User.query.filter_by(id=8172146).first()
            login_user(devuser)
            return redirect('catalog')
# --DEVELOPER LOGIN-REMOVE BEFORE LAUNCH-DEVELOPER LOGIN-REMOVE BEFORE LAUNCH--

    return render_template('catalog.html',
                           categories=categories, items=items, user=user)


# Add a new catagory to the catalog
@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def addCategory():
    user = ''
    if current_user.is_authenticated:
        user = current_user
    if request.method == "POST":
        if Category.query.filter_by(
                        name=request.form.get('newcategory').strip()).first() is not None:
            flash('Category already exists please enter a new category')
        else:
            newcategory = Category(name=request.form.get('newcategory').strip())

            db.session.add(newcategory)
            db.session.commit()
            return redirect('catalog')
    return render_template('addcategory.html', user=user)


# Show all items in a catagory
@app.route('/catalog/<category_name>')
def categories(category_name):
    category = Category.query.filter_by(name=category_name).one()
    items = Item.query.filter_by(category_id=category.id)
    if current_user.is_authenticated:
        user = current_user
    return render_template('category.html', category=category, items=items,
                           user=user)


# Add an item to the catagory
@app.route('/catalog/<category>/add')
@login_required
def addCategories():
    return render_template('catalog.html')


# Update the current catagory
@app.route('/catalog/<category_name>/update')
@login_required
def updateCategories():
    return render_template('index.html')


# Delete the current catagory
@app.route('/catalog/<category_name>/delete')
@login_required
def deleteCategories():
    return render_template('index.html')


# Show item details
@app.route('/catalog/<category_name>/<item>')
def items():
    return render_template('index.html')


# Update item details
@app.route('/catalog/<category_name>/<item>/update')
@login_required
def updateItems():
    return render_template('index.html')


# Delete item
@app.route('/catalog/<category_name>/<item>/delete')
@login_required
def deleteItems():
    return render_template('index.html')


# json data for catalog page
@app.route('/catalog/json')
def jsonCatalog():
    categories = Category.query.all()
    response = category_schema.dumps(categories, indent=2,
                                     separators=(',', ':')).data
    return render_template('jsonresults.html', response=response)


# json data for a catagory page
@app.route('/catalog/<category_name>/json')
def jsonCategories():
    return render_template('index.html')


# json data for an item
@app.route('/catalog/<category_name>/<item>/json')
def jsonItems():
    return render_template('index.html')
