__author__ = 'dmertl'

from flask import Flask, session
import foursquare

app = Flask(__name__)
app.config.from_pyfile('config.py')

from foursquarelocal.database import db_session


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def get_client(access_token=None):
    """
    Create a new foursquare client

    :param access_token: Optional access token to use for client auth
    :type access_token: str
    :return:
    :rtype: foursquare.Foursquare
    """
    client = foursquare.Foursquare(client_id=app.config['FOURSQUARE_API_CLIENT_ID'],
                                   client_secret=app.config['FOURSQUARE_API_SECRET'],
                                   redirect_uri=app.config['FOURSQUARE_API_REDIRECT_URI'])
    if access_token:
        client.set_access_token(access_token)
    elif 'user' in session:
        client.set_access_token(session['user']['access_token'])
    return client

import foursquarelocal.views
