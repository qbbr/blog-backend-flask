def test_index(client):
    response = client.get("/posts/")
    assert 200 == response.status_code
