DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    foursquare_user_id VARCHAR(255) NOT NULL,
    access_token VARCHAR(255) DEFAULT NULL,
    created DATETIME NOT NULL,
    modified DATETIME DEFAULT NULL
);