from fastapi import APIRouter, HTTPException, Request
from controllers.ai_controller import get_ai_decision_matrix
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("")
async def ai_decision_matrix(request: Request):
    logger.info("ai_decision_matrix handler invoked")

    try:
        payload = await request.json()
    except Exception:
        raw_body = (await request.body()).decode(errors="ignore")
        logger.exception("Failed to parse request body as JSON. Raw body=%s", raw_body)
        raise HTTPException(status_code=400, detail="Request body must be valid JSON")

    logger.info("Received AI decision matrix payload: %s", payload)

    if isinstance(payload, dict):
        user_input = payload.get("user_input") or payload.get("input") or payload.get("text")
    elif isinstance(payload, str):
        user_input = payload
    else:
        user_input = None

    if not user_input:
        raise HTTPException(status_code=422, detail="user_input is required")

    logger.info(f"Received AI decision matrix request with input: {user_input}")
    
    return get_ai_decision_matrix(user_input)

