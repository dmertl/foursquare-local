__author__ = 'dmertl'

import models
import flask
import database
import datetime

from foursquarelocal import get_client


def user():
    if 'user' in flask.session:
        return models.User.query.filter_by(id=flask.session['user']['id']).first()
    else:
        return None


def login(access_token):
    _user = models.User.query.filter_by(access_token=access_token).first()
    if not _user:
        _user = create_user(access_token)
    write_auth_session(_user)


def write_auth_session(_user):
    """

    :param _user:
    :type _user: models.User
    :return:
    :rtype:
    """
    flask.session['user'] = _user.to_dict()


def create_user(access_token):
    client = get_client(access_token)
    fsq_user = client.users()
    if not fsq_user:
        raise Exception('Access token invalid')

    _user = models.User()
    _user.access_token = access_token
    _user.id = fsq_user['user']['id']
    _user.first_name = fsq_user['user']['firstName']
    _user.last_name = fsq_user['user']['lastName']
    _user.created = datetime.datetime.now()
    database.db_session.add(_user)
    database.db_session.commit()
    return _user
