from pydantic import BaseModel, HttpUrl
from typing import List

class CodeReviewRequest(BaseModel):
    assignment_description: str
    github_repo_url: HttpUrl
    candidate_level: str

class CodeReviewResponse(BaseModel):
    found_files: List[str]
    downsides_comments: str
    rating: int