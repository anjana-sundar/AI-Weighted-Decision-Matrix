import asyncio
import json
import logging
import os
import httpx
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
MODEL = "command-r-plus"
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
    request_body = {
        "model": MODEL,
        "message": f"Generate a JSON based on this input: {user_input}",
        "preamble": SYSTEM_INSTRUCTION,
        "temperature": 0.6,
        "response_format": {"type": "json_object"}
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {COHERE_API_KEY}",
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                json=request_body,
            )
            response.raise_for_status()
            result = response.json()
            
            parsed_result = json.loads(result["text"])
            
            return JSONResponse(
                content={
                    "success": True,
                    "data": parsed_result,
                }
            )
            
        except httpx.HTTPStatusError as exc:
            logger.error("HTTP error from Cohere: %s", exc.response.text)
            raise HTTPException(
                status_code=502,
                detail=f"Cohere API error: {exc.response.text}"
            ) from exc
            
        except (KeyError, TypeError, ValueError) as exc:
            logger.exception("Cohere API returned an invalid JSON response")
            raise HTTPException(
                status_code=502,
                detail="Cohere returned malformed JSON data"
            ) from exc
