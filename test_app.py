import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.data == b'Hello, World!'

def test_health(client):
    response = client.get('/health')
    assert response.json == {'status': 'UP'}

