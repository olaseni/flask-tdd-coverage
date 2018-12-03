import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext
from click import command


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    db.executescript('''
-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS person;

CREATE TABLE person (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL,
  date_of_birth TEXT NOT NULL,
  address TEXT NOT NULL,
  profession TEXT NOT NULL,
  notes TEXT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  modified TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);
    ''')


@command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()


def init(app):
    """Register database functions with the app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
