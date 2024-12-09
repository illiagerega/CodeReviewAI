# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_review_code():
    response = client.post("/review", json={
        "assignment_description": "Implement a sorting algorithm.",
        "github_repo_url": "https://api.github.com/repos/username/repo_name/contents/",
        "candidate_level": "Junior"
    })
    assert response.status_code == 200
    assert "found_files" in response.json()