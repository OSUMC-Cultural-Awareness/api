def test_list_admins(client):
    res = client.get("/v1/admin")
    assert res.get_json()["admins"] == ["admin@gmail.com"]

    res = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.get("/v1/admin")
    assert res.get_json()["admins"] == ["admin@gmail.com", "tester@gmail.com"]


def test_login(client):
    res = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.post(
        "/v1/login", json={"email": "tester@gmail.com", "password": "password"}
    )
    assert res.status_code == 200
    assert res.get_json()["token"] is not None


def test_login_invalid(client):
    res = client.post(
        "/v1/login", json={"email": "admin@gmail.com", "password": "not-the-password"}
    )
    assert res.status_code == 401


def test_invalid_jwt(client):
    res = client.get("v1/admin", headers={"Authorization": "Bearer " + "this-is-fake"})
    assert res.status_code == 422


def test_create_admin(client):
    res = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )
    assert res.status_code == 201
    assert res.get_json()["token"] is not None


def test_create_admin_duplicate(client):
    res = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    assert res.status_code == 201

    res1 = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    assert res1.status_code == 409

    assert res1.get_json() == {
        "msg": "failed to create admin with email <tester@gmail.com>: duplicate"
    }


def test_get_admin(client):
    res = client.get("/v1/admin/admin@gmail.com")
    res.get_json() == {
        "name": "admin",
        "email": "admin@gmail.com",
    }


def test_delete_admin(client):
    res = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )
    res = client.delete("/v1/admin/tester@gmail.com")
    assert res.get_json() == {"msg": "successfully deleted admin <tester@gmail.com>"}


def test_update_admin(client):
    res = client.post(
        "/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.put(
        "/v1/admin/tester@gmail.com",
        json={
            "name": "tester-different-name",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    assert res.get_json() == {"msg": "successfully updated admin <tester@gmail.com>"}

    res = client.get("/v1/admin")
    assert res.get_json() == {"admins": ["admin@gmail.com", "tester@gmail.com"]}
