DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    access_token TEXT DEFAULT NULL,
    created NUMERIC NOT NULL
);

DROP TABLE IF EXISTS checkins;

CREATE TABLE checkins (
    id TEXT PRIMARY KEY,
    createdAt NUMERIC NOT NULL,
    modified NUMERIC NOT NULL,
    venue_id TEXT
);

DROP TABLE IF EXISTS venues;

CREATE TABLE venues (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location_address TEXT,
    location_cc TEXT,
    location_city TEXT,
    location_country TEXT,
    location_crossStreet TEXT,
    location_lat NUMERIC,
    location_lon NUMERIC,
    location_postalCode TEXT,
    location_state TEXT
);

DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    pluralName TEXT,
    `primary` INTEGER NOT NULL,
    shortName TEXT
);

DROP TABLE IF EXISTS categories_venues;

CREATE TABLE categories_venues (
    category_id TEXT,
    venue_id TEXT
);
