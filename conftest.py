# conftest.py
import os
import pytest
from app import create_app  # Adjust this path based on where your app is located


@pytest.fixture(scope='session', autouse=True)
def set_test_environment():
    # Set the FLASK_ENV to 'test' for the duration of the test session
    os.environ['FLASK_ENV'] = 'test'


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

