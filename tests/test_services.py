import pytest
import aioredis
from fastapi import HTTPException
from app.services import fetch_github_repo_contents, analyze_code_with_openai
from unittest.mock import patch

@pytest.mark.asyncio
async def test_fetch_github_repo_contents(mocker):
    # Mock the HTTPX get function to simulate GitHub API response
    mock_response = {
        "files": [
            {"download_url": "https://raw.githubusercontent.com/user/repo/main/file1.py", "type": "file"},
            {"download_url": "https://raw.githubusercontent.com/user/repo/main/file2.py", "type": "file"}
        ]
    }
    
    # Mocking httpx.get
    mocker.patch('httpx.get', return_value=mock_response)
    
    # Test fetching from GitHub (first call should not use cache)
    response = await fetch_github_repo_contents("https://api.github.com/repos/user/repo/contents/")
    assert response == mock_response
    
    # Test fetching from cache (subsequent call should use cache)
    cached_response = await fetch_github_repo_contents("https://api.github.com/repos/user/repo/contents/")
    assert cached_response == mock_response


@pytest.mark.asyncio
async def test_fetch_github_repo_contents_error(mocker):
    # Mock the HTTPX get function to simulate an error response from GitHub API
    mocker.patch('httpx.get', side_effect=HTTPException(status_code=404, detail="Repository not found"))
    
    with pytest.raises(HTTPException) as exc_info:
        await fetch_github_repo_contents("https://api.github.com/repos/user/nonexistent_repo/contents/")
    assert exc_info.value.status_code == 404
    assert "Repository not found" in str(exc_info.value.detail)


@pytest.mark.asyncio
async def test_analyze_code_with_openai(mocker):
    # Mocking the response from OpenAI API
    mock_response = {
        "choices": [
            {"message": {"content": "Code looks good!"}}
        ]
    }
    
    mocker.patch('httpx.post', return_value=mock_response)

    code = "print('Hello, World!')"
    result = await analyze_code_with_openai(code)
    assert result == "Code looks good!"