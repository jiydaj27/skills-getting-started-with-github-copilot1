from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities_returns_200_and_dict():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # expect some known activities exist
    assert "Chess Club" in data


def test_signup_and_duplicate_returns_error():
    activity = "Basketball Team"
    email = "tester@example.com"

    # Ensure participant not already present
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]

    # Sign up should succeed
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert "Signed up" in res.json()["message"]

    # Duplicate signup should fail with 400
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 400


def test_unregister_removes_participant():
    activity = "Basketball Team"
    email = "remove-me@example.com"

    # Sign up the temporary participant
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200

    # Confirm participant appears
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email in participants

    # Delete/unregister participant
    res = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert "Unregistered" in res.json()["message"]

    # Verify participant no longer present
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email not in participants
