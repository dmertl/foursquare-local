__author__ = 'dmertl'

from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('config.py')

from foursquarelocal.database import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

import foursquarelocal.views
