__author__ = 'dmertl'

import models
import database
import auth
from foursquarelocal import get_client

_cache = {
    "venues": {},
    "categories": {}
}


def sync():
    """
    Sync local database with Foursquare API
    TODO: On first query, start at user's oldest checkin
    TODO: For existing users, query from date of last checkin - a few seconds
    """
    user = auth.user()
    client = get_client()
    checkins = client.users.checkins()
    for fsq_checkin in checkins['checkins']['items']:
        checkin = _create_checkin(fsq_checkin, user)
        database.db_session.add(checkin)
    database.db_session.commit()


def _create_checkin(fsq_checkin, user):
    checkin = models.Checkin.from_foursquare(fsq_checkin, user.id)
    checkin.venue = _create_venue(fsq_checkin['venue'])
    checkin.user = user
    return checkin


def _create_venue(fsq_venue):
    if fsq_venue['id'] in _cache['venues']:
        venue = _cache['venues'][fsq_venue['id']]
    else:
        venue = models.Venue.query.filter_by(id=fsq_venue['id']).first()
    if not venue:
        venue = models.Venue.from_foursquare(fsq_venue)
    for fsq_category in fsq_venue['categories']:
        venue.categories.append(_create_category(fsq_category))
    _cache['venues'][venue.id] = venue
    return venue


def _create_category(fsq_category):
    if fsq_category['id'] in _cache['categories']:
        category = _cache['categories'][fsq_category['id']]
    else:
        category = models.Category.query.filter_by(id=fsq_category['id']).first()
    if not category:
        category = models.Category.from_foursquare(fsq_category)
    _cache['categories'][category.id] = category
    return category
