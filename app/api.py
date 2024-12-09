from fastapi import APIRouter, HTTPException
from app.models import CodeReviewRequest, CodeReviewResponse
from app.services import perform_code_review

router = APIRouter()

@router.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    try:
        review = await perform_code_review(request)
        return review
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))