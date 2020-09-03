from pprint import pprint

post_data = {
    'title': 'my post title 1',
    'text': 'my post long text',
    'tags': [
        {'name': 'tag1'},
        {'name': 'tag2'},
    ],
    'isPrivate': False
}
post_new_data = {
    'title': 'my post title 2',
}
id = None


def test_create(client, auth):
    token = auth.get_token()
    response = client.post('/user/post/', json=post_data, headers={'Authorization': 'Bearer {}'.format(token)})
    assert 201 == response.status_code


def test_get_all(client, auth):
    global id
    token = auth.get_token()
    response = client.get('/user/posts/', headers={'Authorization': 'Bearer {}'.format(token)})
    assert 200 == response.status_code
    data = response.get_json()
    assert 'results' in data
    assert 'page' in data
    assert 'pageSize' in data
    assert 'total' in data
    first_post = data['results'][0]
    assert 'id' in first_post
    id = first_post['id']


def test_get(client, auth):
    global id
    token = auth.get_token()
    response = client.get('/user/post/{}/'.format(id), headers={'Authorization': 'Bearer {}'.format(token)})
    assert 200 == response.status_code
    data = response.get_json()
    assert 'id' in data
    assert id == data['id']
    assert post_data['title'] == data['title']


def test_update(client, auth):
    global id
    token = auth.get_token()
    response = client.put('/user/post/{}/'.format(id), json=post_new_data,
                          headers={'Authorization': 'Bearer {}'.format(token)})
    assert 204 == response.status_code


def test_get_new_data(client, auth):
    global id
    token = auth.get_token()
    response = client.get('/user/post/{}/'.format(id), headers={'Authorization': 'Bearer {}'.format(token)})
    assert 200 == response.status_code
    data = response.get_json()
    assert 'id' in data
    assert id == data['id']
    assert post_new_data['title'] == data['title']


def test_delete(client, auth):
    token = auth.get_token()
    response = client.delete('/user/post/{}/'.format(id), headers={'Authorization': 'Bearer {}'.format(token)})
    assert 204 == response.status_code


def test_delete_all(client, auth):
    token = auth.get_token()
    response = client.delete('/user/posts/', headers={'Authorization': 'Bearer {}'.format(token)})
    assert 204 == response.status_code
