import main


def test_health_endpoint_returns_ok():
    """Health endpoint should return status ok."""
    client = main.app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_note_requires_title():
    """POST /notes without a title should return 400."""
    client = main.app.test_client()
    response = client.post("/notes", json={"body": "no title here"})
    assert response.status_code == 400
    assert "error" in response.get_json()
