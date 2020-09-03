auth_data = {'username': 'testuser2', 'password': 'testpassword2'}


def test_register(client):
    response = client.post('/register/',
                           json=auth_data)
    data = response.get_json()
    assert 201 == response.status_code
    assert 'token' in data


def test_login(client):
    response = client.post('/login/',
                           json=auth_data)
    data = response.get_json()
    assert 200 == response.status_code
    assert 'token' in data
