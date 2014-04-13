__author__ = 'dmertl'

from urllib import urlencode
from pprint import pprint, pformat
import foursquare
from flask import request, render_template, session, flash, abort, redirect, url_for
import auth

from foursquarelocal import app, get_client


@app.route('/')
def home():
    auth_endpoint = 'https://foursquare.com/oauth2/authenticate'
    auth_params = {
        'client_id': app.config['FOURSQUARE_API_CLIENT_ID'],
        'response_type': 'token',
        'redirect_uri': app.config['FOURSQUARE_API_REDIRECT_URI']
    }
    auth_url = auth_endpoint + '?' + urlencode(auth_params)

    return render_template('home.html', auth_url=auth_url)


@app.route('/download_checkins')
def download_checkins():
    if session['user']:
        client = get_client()
        checkins = client.users.checkins()
        return pformat(checkins)
        return render_template('download_checkins.html')
    else:
        abort(401)


@app.route('/access_token_login', methods=['POST'])
def access_token_login():
    """
    Debugging method for inputting an access token directly rather than going through authorization process.
    Can generate access token by making queries to API in browser. See Foursquare auth documentation.
    """
    if request.form['access_token']:
        auth.login(request.form['access_token'])
        return redirect(url_for('home'))
    else:
        raise Exception('No access token provided')



