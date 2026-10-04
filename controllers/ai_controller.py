import json
import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse


load_dotenv()

logger = logging.getLogger(__name__)
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-2.5-flash:generateContent"
)
SYSTEM_INSTRUCTION = """Convert natural decision-making text into structured JSON.

Infer a title, options, criteria, weights, and scores.
Return only valid JSON with this shape:
{
  "title": "",
  "options": [],
  "criteria": [
    {
      "id": "",
      "name": "",
      "weight": 1,
      "scores": {"Option": 1}
    }
  ]
}
Use scores and weights from 1 to 10, infer missing values realistically,
and keep criteria names short."""


async def get_ai_decision_matrix(user_input: str):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Set GEMINI_API_KEY.",
        )

    request_body = {
        "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        "contents": [{"role": "user", "parts": [{"text": user_input}]}],
        "generationConfig": {
            "temperature": 0.6,
            "maxOutputTokens": 4096,
            "responseMimeType": "application/json",
        },
    }

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                GEMINI_API_URL,
                headers={"x-goog-api-key": api_key},
                json=request_body,
            )
    except httpx.TimeoutException as exc:
        logger.exception("Gemini API request timed out")
        raise HTTPException(
            status_code=504,
            detail="AI provider request timed out",
        ) from exc
    except httpx.RequestError as exc:
        logger.exception("Gemini API request failed")
        raise HTTPException(
            status_code=502,
            detail="Could not reach AI provider",
        ) from exc

    if response.is_error:
        logger.error(
            "Gemini API returned HTTP %s: %s",
            response.status_code,
            response.text,
        )
        raise HTTPException(status_code=502, detail="AI provider request failed")

    try:
        result = response.json()
        text = "".join(
            part["text"]
            for part in result["candidates"][0]["content"]["parts"]
            if "text" in part
        )
        parsed_result = json.loads(text)
        if not isinstance(parsed_result, dict):
            raise ValueError("Gemini response must be a JSON object")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        logger.exception("Gemini API returned an invalid decision matrix response")
        raise HTTPException(
            status_code=502,
            detail="AI provider returned an invalid decision matrix",
        ) from exc

    return JSONResponse(content={
        "success": True,
        "data": text,
    })
