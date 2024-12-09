import os
import httpx
from app.models import CodeReviewRequest, CodeReviewResponse
from app.utils import fetch_file_content
import aioredis
from fastapi import HTTPException

# Redis connection setup
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

redis_client = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)

async def fetch_github_repo_contents(github_repo_url: str):
    """
    Fetch the contents of a GitHub repository with caching.
    """
    cache_key = f"repo_contents:{github_repo_url}"
    cached_contents = await redis_client.get(cache_key)

    if cached_contents:
        return cached_contents  # Return cached data if available

    # If not in cache, fetch from GitHub
    try:
        response = await httpx.get(github_repo_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        response.raise_for_status()
        contents = response.json()
        await redis_client.set(cache_key, contents, ex=3600)  # Cache for 1 hour
        return contents
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching repository: {e.response.text}")

async def analyze_code_with_openai(code: str):
    """
    Analyze the code using OpenAI's GPT API.
    
    Parameters:
    - code: The code to analyze.
    
    Returns:
    - The analysis result as a string.
    """
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4-turbo",
        "messages": [{"role": "user", "content": f"Review this code: {code}"}]
    }
    response = await httpx.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json().get("choices")[0]["message"]["content"]

async def perform_code_review(request: CodeReviewRequest) -> CodeReviewResponse:
    repo_contents = await fetch_github_repo_contents(request.github_repo_url)
    
    code_files = [file['download_url'] for file in repo_contents.get('files', []) if file['type'] == 'file']
    review_comments = []

    for file in code_files:
        code_content = await fetch_file_content(file)
        review_comment = await analyze_code_with_openai(code_content)
        review_comments.append(review_comment)

    return CodeReviewResponse(
        found_files=code_files,
        downsides_comments="; ".join(review_comments),
        rating=len(code_files)
    )