def test_list_cultures_empty(client):
    response = client.get("/api/v1/cultures")
    assert response.get_json() == {"cultures": []}


def test_list_cultures(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )

    response1 = client.get("/api/v1/cultures")
    assert response1.get_json() == {
        "cultures": [{"name": "test", "modified": response.get_json()["modified"]}]
    }


def test_create_culture(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "test"
    assert response.get_json()["general_insights"] == []
    assert response.get_json()["specialized_insights"] == []


def test_create_culture_invalid_400(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "names": "test",
        },
    )

    assert response.status_code == 400


def test_create_culture_duplicate(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )

    assert response.status_code == 409


def test_delete_culture(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )

    response1 = client.get("/api/v1/cultures")
    assert response1.get_json() == {
        "cultures": [{"name": "test", "modified": response.get_json()["modified"]}]
    }

    response = client.delete("/api/v1/cultures/test")
    assert response.status_code == 200


def test_delete_culture_invalid_DNE(client):
    response = client.delete("/api/v1/cultures/test")
    assert response.status_code == 404


def test_get_culture(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )

    test = client.get("/api/v1/cultures/test")

    assert test.get_json() == response.get_json()


def test_get_culture_invalid_DNE(client):
    test = client.get("/api/v1/cultures/test1")

    assert test.status_code == 404


def test_update_culture(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )
    response_json = response.get_json()

    update_response = client.put(
        "/api/v1/cultures/test",
        json={
            "name": "test",
            "general_insights": [
                {
                    "summary": "summarizing text",
                    "information": "some interesting information",
                    "source": {
                        "type": "link",
                        "data": "http://www.randomeinformation.com",
                    },
                }
            ],
            "specialized_insights": {},
        },
    )

    update_json = update_response.get_json()
    assert update_json != response_json

    assert update_json["general_insights"][0] == {
        "summary": "summarizing text",
        "information": "some interesting information",
        "source": {"type": "link", "data": "http://www.randomeinformation.com"},
    }


def test_update_culture_invalid_400(client):
    response = client.post(
        "/api/v1/cultures",
        json={
            "name": "test",
        },
    )
    update_response = client.put(
        "/api/v1/cultures/test",
        json={
            "names": "test",
        },
    )

    assert update_response.status_code == 400


def test_update_culture_create(client):
    update_response = client.put(
        "/api/v1/cultures/test",
        json={
            "name": "test",
            "general_insights": [
                {
                    "summary": "summarizing text",
                    "information": "some interesting information",
                    "source": {
                        "type": "link",
                        "data": "http://www.randomeinformation.com",
                    },
                }
            ],
            "specialized_insights": {},
        },
    )

    assert update_response.status_code == 201
