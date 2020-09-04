import pytest

from flaskr import create_app, db
from flaskr.models import User, Post, Tag


@pytest.fixture(scope='module')
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///'})

    with app.app_context():
        db.create_all()
        create_fake_data()

    return app


@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()


def create_fake_data():
    user = User(username='fakeuser1')
    user.setpassword('fakepassword1')
    tag = Tag(name='tag1')
    post = Post(user=user, title='fake title 1', text='fake text 1', tags=[tag])
    db.session.add(user)
    db.session.add(tag)
    db.session.add(post)
    db.session.commit()


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
