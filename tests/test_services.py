import pytest
import aioredis
from app.services import fetch_github_repo_contents
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_fetch_github_repo_contents(mocker):
    # Mock the HTTPX get function to simulate GitHub API response
    mock_response = {
        "files": [
            {"download_url": "https://raw.githubusercontent.com/user/repo/main/file1.py", "type": "file"},
            {"download_url": "https://raw.githubusercontent.com/user/repo/main/file2.py", "type": "file"}
        ]
    }
    
    # Mocking httpx.get and aioredis methods
    mocker.patch('httpx.get', return_value=mock_response)
    
    # Test fetching from GitHub (first call should not use cache)
    response = await fetch_github_repo_contents("https://api.github.com/repos/user/repo/contents/")
    assert response == mock_response
    
    # Test fetching from cache (subsequent call should use cache)
    cached_response = await fetch_github_repo_contents("https://api.github.com/repos/user/repo/contents/")
    assert cached_response == mock_response