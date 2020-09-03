import pytest

from flaskr import create_app, db


@pytest.fixture(scope='module')
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///'})

    with app.app_context():
        db.create_all()

    return app


@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    USERNAME = 'testusername1'
    PASSWORD = 'testpassword1'
    token = ''

    def get_token(self, username=USERNAME, password=PASSWORD):
        if not len(self.token):
            response = self._client.post('/register/',
                                         json={'username': username, 'password': password})
            self.token = response.get_json()['token']
        return self.token


@pytest.fixture(scope='module')
def auth(client):
    return AuthActions(client)
