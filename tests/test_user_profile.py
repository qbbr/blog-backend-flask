profile_new_data = {
    'about': 'new about text',
}


def assert_profile(data):
    assert 'id' in data
    assert 'username' in data
    assert 'about' in data
    assert 'postsCount' in data
    assert 'createdAt' in data


def test_get(client, auth):
    token = auth.get_token()
    response = client.get('/user/profile/', headers={'Authorization': 'Bearer {}'.format(token)})
    assert 200 == response.status_code
    data = response.get_json()
    assert_profile(data)


def test_update(client, auth):
    token = auth.get_token()
    response = client.put('/user/profile/', json=profile_new_data,
                          headers={'Authorization': 'Bearer {}'.format(token)})
    assert 204 == response.status_code


def test_get_new_data(client, auth):
    token = auth.get_token()
    response = client.get('/user/profile/', headers={'Authorization': 'Bearer {}'.format(token)})
    assert 200 == response.status_code
    data = response.get_json()
    assert_profile(data)
    assert profile_new_data['about'] == data['about']


def test_delete(client, auth):
    token = auth.get_token(username='testfordelete', password='testfordelete')
    response = client.delete('/user/profile/', headers={'Authorization': 'Bearer {}'.format(token)})
    assert 204 == response.status_code
