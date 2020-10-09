def test_list_admins(client):
    res = client.get("/v1/admins")
    assert res.get_json()["admins"] == []

    res = client.post(
        "/v1/register",
        json={
            "username": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "test",
        },
    )

    res = client.get("/v1/admins")
    assert res.get_json()["admins"] == ["tester"]


def test_login(client):
    res = client.post(
        "/v1/register",
        json={
            "username": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "test",
        },
    )

    res = client.post(
        "/v1/login", json={"email": "tester@gmail.com", "password": "password"}
    )
    assert res.get_json() == {"message": "Authenticated"}


def test_create_admin(client):
    res = client.post(
        "/v1/register",
        json={
            "username": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "test",
        },
    )
    assert res.get_json() == {
        "message": "successfully created admin tester <tester@gmail.com>"
    }


def test_delete_admin(client):
    res = client.post(
        "/v1/register",
        json={
            "username": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "test",
        },
    )
    res = client.delete("/v1/admin/tester@gmail.com")
    assert res.get_json() == {
        "message": "successfully deleted admin <tester@gmail.com>"
    }


def test_update_admin(client):
    res = client.post(
        "/v1/register",
        json={
            "username": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "test",
        },
    )

    res = client.put(
        "/v1/admin/tester@gmail.com",
        json={
            "username": "tester-different-name",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
            "oauth": "test",
        },
    )

    assert res.get_json() == {
        "message": "successfully updated admin <tester@gmail.com>"
    }

    res = client.get("/v1/admins")
    assert res.get_json() == {"admins": ["tester-different-name"]}
