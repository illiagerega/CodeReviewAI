# tests/test_services.py
import pytest
from app.services import analyze_code_with_openai

@pytest.mark.asyncio
async def test_analyze_code_with_openai():
    code = "print('Hello, World!')"
    review = await analyze_code_with_openai(code)
    assert isinstance(review, str)