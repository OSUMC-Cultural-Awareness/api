def test_list_admins(client):
    res = client.get("/api/v1/admins")
    print(res)
    assert res.get_json()["admins"] == [
        {"email": "admin@gmail.com", "name": "admin", "superUser": False}
    ]

    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.get("/api/v1/admins")
    assert res.get_json()["admins"] == [
        {"email": "admin@gmail.com", "name": "admin", "superUser": False},
        {"email": "tester@gmail.com", "name": "tester", "superUser": False},
    ]


def test_login(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.post(
        "/api/v1/login", json={"email": "tester@gmail.com", "password": "password"}
    )
    assert res.status_code == 200
    json = res.get_json()
    assert json["token"] is not None
    admin = json["user"]

    assert admin["_id"] is not None

    del admin["_id"]
    assert admin == {"name": "tester", "email": "tester@gmail.com", "superUser": False}


def test_login_invalid_bad_password(client):
    res = client.post(
        "/api/v1/login",
        json={"email": "admin@gmail.com", "password": "not-the-password"},
    )
    assert res.status_code == 401


def test_login_invalid_bad_email(client):
    res = client.post(
        "/api/v1/login",
        json={"email": "admins@gmail.com", "password": "not-the-password"},
    )
    assert res.status_code == 401


def test_login_invalid_400(client):
    res = client.post(
        "/api/v1/login",
        json={"email": "admin@gmail.com", "passwordss": "not-the-password"},
    )
    assert res.status_code == 400


def test_invalid_jwt(client):
    res = client.get(
        "/api/v1/admins", headers={"Authorization": "Bearer " + "this-is-fake"}
    )
    assert res.status_code == 422


def test_create_admin(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )
    assert res.status_code == 201
    json = res.get_json()
    assert json["token"] is not None

    admin = json["user"]
    assert admin["_id"] is not None
    del admin["_id"]

    assert admin == {"name": "tester", "email": "tester@gmail.com", "superUser": False}


def test_create_admin_invalid_400(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "passwords": "password",
            "password_confirmation": "password",
        },
    )
    assert res.status_code == 400


def test_create_admin_invalid_password_and_confirm_dont_match(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password-test",
            "password_confirmation": "password",
        },
    )
    assert res.status_code == 401


def test_create_admin_duplicate(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    assert res.status_code == 201

    res1 = client.post(
        "/api/v1/register",
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
    res = client.get("/api/v1/admins/admin@gmail.com")
    res.get_json() == {
        "name": "admin",
        "email": "admin@gmail.com",
    }


def test_get_admin_invalid_no_admin(client):
    res = client.get("/api/v1/admins/admins@gmail.com")
    assert res.get_json()["msg"] == "unknown admin `admins@gmail.com`"
    assert res.status_code == 404


def test_delete_admin(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )
    res = client.delete("/api/v1/admins/tester@gmail.com")
    assert res.get_json() == {"msg": "successfully deleted admin <tester@gmail.com>"}


def test_update_admin(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.put(
        "/api/v1/admins/tester@gmail.com", json={"name": "tester-different-name",},
    )

    assert res.get_json() == {"msg": "successfully updated admin <tester@gmail.com>"}

    res = client.get("/api/v1/admins")
    assert res.get_json()["admins"] == [
        {"email": "admin@gmail.com", "name": "admin", "superUser": False},
        {
            "email": "tester@gmail.com",
            "name": "tester-different-name",
            "superUser": False,
        },
    ]


def test_update_admin_invalid_400(client):
    res = client.post(
        "/api/v1/register",
        json={
            "name": "tester",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    res = client.put(
        "/api/v1/admins/tester@gmail.com",
        json={
            "names": "tester-different-name",
            "email": "tester@gmail.com",
            "password": "password",
            "password_confirmation": "password",
        },
    )

    assert res.status_code == 400


def test_send_invite_email(client):
    res = client.post("/api/v1/admins/invite", json={"email": "test@gmail.com"})
    assert res.status_code == 200
    assert res.get_json() == {"msg": "email sent to test@gmail.com"}


def test_send_invite_email_duplicate(client):
    res = client.post("/api/v1/admins/invite", json={"email": "admin@gmail.com"})
    assert res.status_code == 409

    assert res.get_json() == {"msg": "<admin@gmail.com>: duplicate"}


def test_send_invite_email_invalid(client):
    res = client.post("/api/v1/admins/invite", json={"emails": "admin@gmail.com"})
    assert res.status_code == 400


def test_recover_email(client):
    res = client.post("/api/v1/admins/recover", json={"email": "admin@gmail.com"})
    assert res.status_code == 200


def test_recover_email_unknown(client):
    res = client.post("/api/v1/admins/recover", json={"email": "unknown@gmail.com"})
    assert res.status_code == 404


def test_recover_email_invalid(client):
    res = client.post("/api/v1/admins/recover", json={"emails": "admin@gmail.com"})
    assert res.status_code == 400
