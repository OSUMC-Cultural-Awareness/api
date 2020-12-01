"""Pytest setup."""
import mongomock  # type: ignore
import pytest  # type: ignore
from werkzeug.security import generate_password_hash

from api import create_app
from api.auth import auth_routes
from api.resource.admin import admin_routes
from api.resource.culture import culture_routes


def login_admin(flask_client):
    """Login to default admin for testing.

    Arguments:
        flask_client: Flask test client
    """
    res = flask_client.post(
        "/api/v1/login", json={"email": "admin@gmail.com", "password": "password"}
    )

    json = res.get_json()
    assert json["token"] is not None

    return json["token"]


@pytest.fixture
def client():
    """Constructs Flask test client."""
    db = mongomock.MongoClient().db
    app = create_app()
    app.config["SECRET_KEY"] = "testing"

    auth_routes(app, db)
    admin_routes(app, db)
    culture_routes(app, db)
    app.config["TESTING"] = True

    # Create test user
    db.admins.insert_one(
        {
            "name": "admin",
            "email": "admin@gmail.com",
            "password": generate_password_hash("password"),
            "superUser": False,
        }
    )

    flask_client = app.test_client()
    token = login_admin(flask_client)
    flask_client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + token

    yield flask_client
