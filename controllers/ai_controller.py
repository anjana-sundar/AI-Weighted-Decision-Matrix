import asyncio
import json
import logging
import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse

load_dotenv()

logger = logging.getLogger(__name__)

# Primary and fallback model endpoints
PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-1.5-flash"
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

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


async def call_gemini_with_retry(
    client: httpx.AsyncClient,
    model: str,
    api_key: str,
    payload: dict,
    max_retries: int = 3,
) -> dict:
    """Sends a generateContent request with exponential backoff on 503 and 429."""
    url = f"{API_BASE_URL}/{model}:generateContent"

    for attempt in range(max_retries):
        try:
            response = await client.post(
                url,
                headers={"x-goog-api-key": api_key},
                json=payload,
            )

            # Retry on 503 (Overloaded) and 429 (Transient rate limit)
            if response.status_code in (503, 429):
                wait_time = 2**attempt  # 1s, 2s, 4s...
                logger.warning(
                    "Model %s returned HTTP %s (attempt %s/%s). Retrying in %ss...",
                    model,
                    response.status_code,
                    attempt + 1,
                    max_retries,
                    wait_time,
                )
                await asyncio.sleep(wait_time)
                continue

            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as exc:
            # If not a retryable code, fail fast
            logger.error("HTTP error from Gemini %s: %s", model, exc.response.text)
            raise
        except (httpx.TimeoutException, httpx.RequestError) as exc:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2**attempt)

    raise httpx.HTTPStatusError(
        f"Model {model} unavailable after {max_retries} attempts",
        request=None,  # type: ignore
        response=response,
    )


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

    result = None
    async with httpx.AsyncClient(timeout=45.0) as client:
        # 1. Attempt with primary model
        try:
            result = await call_gemini_with_retry(
                client, PRIMARY_MODEL, api_key, request_body
            )
        except Exception as exc:
            logger.warning(
                "Primary model %s failed: %s. Attempting fallback to %s...",
                PRIMARY_MODEL,
                exc,
                FALLBACK_MODEL,
            )
            # 2. Attempt with fallback model
            try:
                result = await call_gemini_with_retry(
                    client, FALLBACK_MODEL, api_key, request_body
                )
            except Exception as final_exc:
                logger.exception("Both primary and fallback models failed")
                raise HTTPException(
                    status_code=502,
                    detail="AI provider is currently unavailable. Please try again later.",
                ) from final_exc

    # Parse and validate the JSON candidate
    try:
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
            detail="AI provider returned an invalid decision matrix structure",
        ) from exc

    return JSONResponse(
        content={
            "success": True,
            "data": parsed_result,
        }
    )
