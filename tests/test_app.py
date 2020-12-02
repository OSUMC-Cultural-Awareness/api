def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200

    assert response.get_json() == {"msg": "healthy"}


def test_feedback(client):
    res = client.post("/api/v1/feedback", json={"feedback": "this is a test"})
    assert res.status_code == 200


def test_feedback_invalid_request(client):
    res = client.post("/api/v1/feedback", json={"feedbacks": "this is a test"})
    assert res.status_code == 400


def test_feedback_invalid_too_short(client):
    res = client.post("/api/v1/feedback", json={"feedback": ""})
    assert res.status_code == 400


def test_feedback_invalid_too_long(client):
    res = client.post("/api/v1/feedback", json={"feedback": "hi" * 300})
    assert res.status_code == 400
