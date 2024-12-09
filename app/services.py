import os
import httpx
from app.models import CodeReviewRequest, CodeReviewResponse
from app.utils import fetch_file_content
from fastapi import HTTPException

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

async def fetch_github_repo_contents(github_repo_url: str):
    """
    Fetch the contents of a GitHub repository.
    
    Parameters:
    - github_repo_url: The URL of the GitHub repository.
    
    Returns:
    - JSON response containing the repository contents.
    """
    try:
        response = await httpx.get(github_repo_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        response.raise_for_status()
        return response.json()
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
    
    # Assuming repo_contents has the structure that contains file URLs
    code_files = [file['download_url'] for file in repo_contents.get('files', []) if file['type'] == 'file']
    review_comments = []

    for file in code_files:
        # Fetch file content using the utility function
        code_content = await fetch_file_content(file)
        review_comment = await analyze_code_with_openai(code_content)
        review_comments.append(review_comment)

    return CodeReviewResponse(
        found_files=code_files,
        downsides_comments="; ".join(review_comments),
        rating=len(code_files)  # Example rating based on number of files
    )