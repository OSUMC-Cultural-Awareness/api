def test_list_cultures_empty(client):
    response = client.get("/v1/culture_groups")
    assert response.get_json() == {"cultures": []}


def test_list_cultures(client):
    response = client.post(
        "v1/culture_groups",
        json={
            "name": "test",
            "oauth": "test",
            "general_insights": [],
            "specialized_insights": [],
        },
    )

    response = client.get("/v1/culture_groups")
    assert response.get_json() == {"cultures": ["test"]}


def test_delete_culture(client):
    response = client.post(
        "v1/culture_groups",
        json={
            "name": "test",
            "oauth": "test",
            "general_insights": [],
            "specialized_insights": [],
        },
    )

    response = client.get("/v1/culture_groups")
    assert response.get_json() == {"cultures": ["test"]}

    response = client.delete("v1/test")
    assert response.status_code == 200


def test_detailed_culture(client):
    response = client.post(
        "v1/culture_groups",
        json={
            "name": "test",
            "oauth": "test",
            "general_insights": [],
            "specialized_insights": [],
        },
    )

    test = client.get("/v1/test/all")

    assert test.get_json() == response.get_json()


def test_snapshot_culture(client):
    response = client.post(
        "v1/culture_groups",
        json={
            "name": "test",
            "oauth": "test",
            "general_insights": [],
            "specialized_insights": [],
        },
    )
    response_json = response.get_json()

    del response_json["specialized_insights"]
    test = client.get("/v1/test")

    assert test.get_json() == response.get_json()


def test_update_culture(client):
    response = client.post(
        "v1/culture_groups",
        json={
            "name": "test",
            "oauth": "test",
            "general_insights": [],
            "specialized_insights": [],
        },
    )
    response_json = response.get_json()

    update_response = client.post(
        "v1/culture_groups",
        json={
            "name": "test",
            "oauth": "test",
            "general_insights": ["idk"],
            "specialized_insights": [],
        },
    )

    update_json = update_response.get_json()
    assert update_json != response_json

    assert update_json["general_insights"][0] == "idk"
