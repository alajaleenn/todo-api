from app import app 


def test_home():
    client= app.test_client()
    response= client.get("/")
    assert response.status_code == 200

def test_todos_requires_token():
    client = app.test_client()
    response = client.get("/todos")
    assert response.status_code == 401