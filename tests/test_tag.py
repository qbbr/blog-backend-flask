def test_index(client):
    response = client.get("/tags/")
    assert 200 == response.status_code
