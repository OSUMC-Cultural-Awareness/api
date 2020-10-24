import mongomock  # type: ignore
import pytest  # type: ignore

from flask import Flask
from flask_bcrypt import Bcrypt  # type: ignore

from . import create_app
from .auth import auth


def login_admin(client):
    res = client.post(
        "/v1/login", json={"email": "admin@gmail.com", "password": "password"}
    )

    json = res.get_json()
    assert json["token"] is not None

    return json["token"]


@pytest.fixture
def client():
    db = mongomock.MongoClient().db
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "testing"
    bcrypt = Bcrypt(app)

    auth(app, db, bcrypt)
    create_app(app, db)
    app.config["TESTING"] = True

    # Create test user
    db.admins.insert_one(
        {
            "name": "admin",
            "email": "admin@gmail.com",
            "password": bcrypt.generate_password_hash("password"),
        }
    )

    client = app.test_client()
    token = login_admin(client)
    client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + token

    yield client
