__author__ = 'dmertl'

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
from pprint import pprint, pformat
from urllib import urlencode
import foursquare

app = Flask(__name__)
app.config.from_pyfile('config.py')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    # Initialize database
    g.db = connect_db()
    g.db.row_factory = make_dicts


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


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


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Development Server Help')
    parser.add_argument("-d", "--debug", action="store_true", dest="debug_mode",
                        help="run in debug mode (for use with PyCharm)", default=False)
    parser.add_argument("-p", "--port", dest="port",
                        help="port of server (default:%(default)s)", type=int, default=5000)

    cmd_args = parser.parse_args()
    app_options = {"port": cmd_args.port}

    if cmd_args.debug_mode:
        app_options["debug"] = True
        app_options["use_debugger"] = False
        app_options["use_reloader"] = False

    app.run(**app_options)
