from fastapi.testclient import TestClient
from app.main import app
from fastapi import HTTPException

client = TestClient(app)

def test_review_code_success(mocker):
    # Mock the perform_code_review function to return a successful response
    mock_response = {
        "found_files": [
            "https://raw.githubusercontent.com/user/repo/main/file1.py",
            "https://raw.githubusercontent.com/user/repo/main/file2.py"
        ],
        "downsides_comments": "Good code; Needs comments.",
        "rating": 2
    }

    mocker.patch('app.services.perform_code_review', return_value=mock_response)

    response = client.post("/review", json={
        "assignment_description": "Implement a sorting algorithm.",
        "github_repo_url": "https://api.github.com/repos/user/repo/contents/",
        "candidate_level": "Junior"
    })

    assert response.status_code == 200
    assert response.json() == mock_response


def test_review_code_failure(mocker):
    # Mock the perform_code_review function to raise an exception
    mocker.patch('app.services.perform_code_review', side_effect=HTTPException(status_code=500, detail="Internal Server Error"))

    response = client.post("/review", json={
        "assignment_description": "Implement a sorting algorithm.",
        "github_repo_url": "https://api.github.com/repos/user/repo/contents/",
        "candidate_level": "Junior"
    })

    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}