import mongomock
import pytest

from . import create_app


@pytest.fixture
def client():
    db = mongomock.MongoClient().db
    app = create_app(db)
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client
