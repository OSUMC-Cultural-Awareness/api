def test_list_cultures_empty(client):
    response = client.get("/v1/culture")
    assert response.get_json() == {"cultures": []}


def test_list_cultures(client):
    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )

    response = client.get("/v1/culture")
    assert response.get_json() == {"cultures": ["test"]}


def test_create_culture(client):
    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["name"] == "test"
    assert response.get_json()["general_insights"] == []
    assert response.get_json()["specialized_insights"] == []


def test_create_culture_duplicate(client):
    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )

    assert response.status_code == 409


def test_delete_culture(client):
    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )

    response = client.get("/v1/culture")
    assert response.get_json() == {"cultures": ["test"]}

    response = client.delete("v1/culture/test")
    assert response.status_code == 200


def test_detailed_culture(client):
    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )

    test = client.get("/v1/culture/test")

    assert test.get_json() == response.get_json()


def test_update_culture(client):
    response = client.post(
        "v1/culture",
        json={
            "name": "test",
        },
    )
    response_json = response.get_json()

    update_response = client.put(
        "v1/culture/test",
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
            "specialized_insights": [],
        },
    )

    update_json = update_response.get_json()
    assert update_json != response_json

    assert update_json["general_insights"][0] == {
        "summary": "summarizing text",
        "information": "some interesting information",
        "source": {"type": "link", "data": "http://www.randomeinformation.com"},
    }
