import httpx
import os
from fastapi import HTTPException

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

async def fetch_file_content(file_url: str) -> str:
    """
    Fetch the content of a file from GitHub.
    
    Parameters:
    - file_url: The raw URL of the file in the repository.
    
    Returns:
    - The content of the file as a string.
    """
    try:
        response = await httpx.get(file_url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        response.raise_for_status()
        return response.text
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching file: {e.response.text}")