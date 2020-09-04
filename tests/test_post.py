post_slug = None


def assert_paginated_posts(data):
    assert 'results' in data
    assert 'page' in data
    assert 'pageSize' in data
    assert 'total' in data


def assert_post(data):
    assert 'id' in data
    assert 'slug' in data
    assert 'title' in data
    assert 'html' in data
    assert 'createdAt' in data


def test_get_all(client):
    global post_slug
    response = client.get('/posts/')
    assert 200 == response.status_code
    data = response.get_json()
    assert_paginated_posts(data)
    first_post = data['results'][0]
    assert_post(first_post)
    post_slug = first_post['slug']


def test_get_by_slug(client):
    response = client.get('/post/{}/'.format(post_slug))
    assert 200 == response.status_code
    data = response.get_json()
    assert_post(data)
