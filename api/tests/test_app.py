import pytest

from cultural_awareness import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200

    index = response.get_json()
    routes = index["routes"]
    assert len(routes) == 16


def test_health(client):
    response = client.get("/v1/health")
    assert response.status_code == 200

    assert response.get_json() == {"message": "healthy"}
