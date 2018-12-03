import sqlite3

import pytest
from datetime import date
from application.persistence import get_db


def test_get_close_db(app_context):
    """
    GIVEN a flask app context
    WHEN a db connection connection is requested multiple times
    THEN ascertain the connection is reused
    """
    with app_context():
        db = get_db()
        assert db is get_db()
        assert db is get_db()

    """
    GIVEN a db connection obtained outside a flask app context
    WHEN a query is executed within this invalid context
    THEN ascertain that the database should be closed
    """
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    assert 'closed' in str(e)


# noinspection SpellCheckingInspection
def test_init_db_command_and_select(runner, monkeypatch, app_context):
    """
    GIVEN a flask cli runner
    WHEN `init-db` is pseudo-invoked from the command line
    THEN check that the output contains a success response substring
    """
    monkeypatch.setattr('application.persistence.init_db', lambda: None)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output

    """
    GIVEN a db connection
    WHEN a read query is executed
    THEN check that output returned is as expected for sqlite db
    """
    with app_context():
        db = get_db()
        now = db.execute('SELECT "now"').fetchone()
        assert 'now' in now

        now = db.execute('SELECT date("now")').fetchone()
        assert date.today().strftime('%Y-%m-%d') in now
