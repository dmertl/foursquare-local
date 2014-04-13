__author__ = 'dmertl'

from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship

from foursquarelocal.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(String(24), primary_key=True)
    access_token = Column(String(48), default=None)
    first_name = Column(String(64), nullable=True)
    last_name = Column(String(64), nullable=True)
    created = Column(DateTime(), nullable=False)
    checkins = relationship('Checkin', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User #{0} {1} {2}>'.format(self.id, self.first_name, self.last_name)

    def to_dict(self):
        return {
            'id': self.id,
            'access_token': self.access_token,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created': self.created
        }


categories_venues = Table(
    'categories_venues', Base.metadata,
    Column('category_id', String(24), ForeignKey('categories.id')),
    Column('venue_id', String(24), ForeignKey('venues.id'))
)


class Venue(Base):
    __tablename__ = 'venues'

    id = Column(String(24), primary_key=True)
    name = Column(String(), nullable=False)
    location_address = Column(String(), default=None)
    location_cc = Column(String(), default=None)
    location_city = Column(String(), default=None)
    location_country = Column(String(), default=None)
    location_crossStreet = Column(String(), default=None)
    location_lat = Column(Float(), default=None)
    location_lon = Column(Float(), default=None)
    location_postalCode = Column(String(), default=None)
    location_state = Column(String(), default=None)
    checkins = relationship('Checkin', backref='venue', lazy='dynamic')
    categories = relationship('Category', secondary=categories_venues)

    def __repr__(self):
        return '<Venue {0}>'.format(self.name)


class Category(Base):
    __tablename__ = 'categories'

    id = Column(String(24), primary_key=True)
    name = Column(String(), nullable=False)
    pluralName = Column(String(), default=None)
    primary = Column(Boolean(), nullable=False)
    shortName = Column(String(), default=None)
    venues = relationship('Venue', secondary=categories_venues)

    def __repr__(self):
        return '<Category {0}>'.format(self.name)


class Checkin(Base):
    __tablename__ = 'checkins'

    id = Column(String(24), primary_key=True)
    createdAt = Column(DateTime(), nullable=False)
    user_id = Column(String(24), ForeignKey('users.id'))
    venue_id = Column(String(24), ForeignKey('venues.id'))

    def __repr__(self):
        return '<Checkin {0}>'.format(self.id)
