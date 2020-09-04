def test_index(client):
    response = client.get('/tags/')
    assert 200 == response.status_code
    data = response.get_json()
    first_tag = data[0]
    assert 'id' in first_tag
    assert 'name' in first_tag
    assert 'postsCount' in first_tag
