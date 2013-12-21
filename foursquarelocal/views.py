__author__ = 'dmertl'

from urllib import urlencode
from pprint import pprint, pformat
import foursquare
from flask import request, render_template, session, flash, abort

from foursquarelocal import app


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
    #JQE0TMHVGYL2DMVPLY0Q5V0QLBXOV2R5OTZOGIUDX0LOQZ1B
    if session['user']:
        client = foursquare.Foursquare(client_id=app.config['FOURSQUARE_API_CLIENT_ID'],
                                       client_secret=app.config['FOURSQUARE_API_SECRET'],
                                       redirect_uri=app.config['FOURSQUARE_API_REDIRECT_URI'])
        client.set_access_token(session['user']['access_token'])
        checkins = client.users.checkins()
        return pformat(checkins)
        return render_template('download_checkins.html')
    else:
        abort(401)


@app.route('/masquerade')
def masquerade():
    if request.args['user_id']:
        user = query_db('SELECT * FROM users WHERE id = ?', [request.args['user_id']], True)
        if user:
            session['user'] = user
            flash('Masquerading as user {0}'.format(user['id']))
            return render_template('masquerade.html')
        else:
            raise Exception('User does not exist')
    else:
        raise Exception('Must provide a user id')
