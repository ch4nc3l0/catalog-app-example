# Catalog-App-Example
Catalog-App-Example is a website witten in python, html, sass, and javascript. The goal of this website/webapp is to increase my skills as a full-stack-developer, and share the knowledge i gained. The website is currently deployed using Heroku [link here](https://catalog-app-example.herokuapp.com/catalog).
# Local Installation
To run a local version of this webapp a file named .env will need to be created with the following information:
- DATABASE_URL='postgres://your_db_link'
- SUPER_SECRET_KEY='your_secret_key'
- GIT_CLIENT_ID='your_git_client_id'
- GIT_CLIENT_SECRET='your_git_secret'

Instructions for attaining a git client and secret can be found [here](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app/)

## How to run a heroku deployed app locally
A great tool for Heroku-apps that use python as the backend is Honcho, it builds and launches the application using the Procfile just like Heroku does. Honcho can be installed using pip:
```
pip install honcho
```
To run the app after installing Honcho simply navigate to the directory of the app and use:
```
honcho start
```
Honcho will automatically find the Procfile and build the app.


## Database setup
Postgres was used in Catalog-App-Example. To setup the database for the first time the following commands can be set in the Procfile then launched with Honcho, use them one at a time.
```
release: python manage.py db init
release: python manage.py db migrate
release: python manage.py db upgrade
```
This will create a new empty database for the app, as long as the enviroment variables are set correctly.


## Dependencies
To run Catalog-App-Example from a local machine the following dependencies must be installed:
- flask==1.0.2
- flask-login==0.4.1
- flask_marshmallow==0.9.0
- flask-migrate==2.3.1
- flask_script==2.0.6
- flask_sqlalchemy==2.3.1
- gunicorn==19.9.0
- marshmallow-sqlalchemy==0.16.0
- psycopg2-binary==2.7.6.1
- requests_oauthlib==1.2.0

## Changes needed in the Procfile
The Procfile will also need to be edited to the port the web app should be seen at:
```
web: gunicorn -b 127.0.0.1:5000 index:app
``` 
This command will launch the app at http://127.0.0.1:5000 change the address as needed.

# Api

Their are currently some basic api calls implemented:
- https://catalog-app-example.herokuapp.com/catalog/json calls all categories and the top 15 most recent items.
- https://catalog-app-example.herokuapp.com/catalog/(category)/json calls all items inside that category.
- https://catalog-app-example.herokuapp.com/(item)/json calls all information about that item.

# Attributions
- This website was developed as part of the full-stack nanodegree from Udacity.

# License
MIT License

Copyright (c) [2019] [Chance Gurley]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.