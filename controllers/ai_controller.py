import json
import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse


load_dotenv()

logger = logging.getLogger(__name__)
MODEL = "command-r-plus-08-2024"
API_URL = "https://api.cohere.com/v1/chat"

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
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured. Set COHERE_API_KEY.",
        )

    request_body = {
        "model": MODEL,
        "message": f"Generate a JSON based on this input: {user_input}",
        "preamble": SYSTEM_INSTRUCTION,
        "temperature": 0.6,
        "response_format": {"type": "json_object"},
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                json=request_body,
            )
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        logger.exception("Cohere API request timed out")
        raise HTTPException(
            status_code=504,
            detail="AI provider request timed out.",
        ) from exc
    except httpx.HTTPStatusError as exc:
        logger.error(
            "Cohere API returned HTTP %s: %s",
            exc.response.status_code,
            exc.response.text,
        )
        raise HTTPException(
            status_code=502,
            detail=f"AI provider request failed (HTTP {exc.response.status_code}).",
        ) from exc
    except httpx.RequestError as exc:
        logger.exception("Could not reach Cohere API")
        raise HTTPException(
            status_code=502,
            detail="Could not reach the AI provider.",
        ) from exc

    try:
        result = response.json()
        parsed_result = json.loads(result["text"])
        if not isinstance(parsed_result, dict):
            raise ValueError("Cohere response must contain a JSON object")
    except (KeyError, TypeError, ValueError) as exc:
        logger.exception("Cohere API returned an invalid JSON response")
        raise HTTPException(
            status_code=502,
            detail="AI provider returned an invalid decision matrix.",
        ) from exc

    return JSONResponse(
        content={
            "success": True,
            "data": parsed_result,
        }
    )
