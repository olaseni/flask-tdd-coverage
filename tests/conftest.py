import os
import tempfile

import pytest
from application import get_app
from application.persistence import init_db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = get_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # create the database and load test data
    with app.app_context():
        init_db()

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def app_context(app):
    """A context function for app-related resources """
    return app.app_context
