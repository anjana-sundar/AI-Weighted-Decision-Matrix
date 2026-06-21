import os

from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from groq import Groq


load_dotenv()


def get_ai_decision_matrix(
    user_input: str
):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    completion = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
        {
            "role": "system",
            "content": "Convert natural decision-making text into structured JSON.\n\nInfer:\n- title\n- options\n- criteria\n- weights\n- scores\n\nRules:\n- Return ONLY valid JSON\n- No markdown\n- Scores: 1-10\n- Weights: 1-10\n- Infer missing values realistically\n- Keep criteria names short\n\nFormat:\n{\n  \"title\": \"\",\n  \"options\": [],\n  \"criteria\": [\n    {\n      \"id\": \"\",\n      \"name\": \"\",\n      \"weight\": 1,\n      \"scores\": {\n        \"Option\": 1\n      }\n    }\n  ]\n}"
        },
        {
            "role": "user",
            "content": user_input
        }
        ],
        temperature=0.6,
        max_completion_tokens=4096,
        top_p=0.95,
        reasoning_effort="default",
        stream=False,
        response_format={"type": "json_object"},
        stop=None
    )
    
    #print(completion.choices[0].message)
    return JSONResponse(content={
        "success": True,
        "data": completion.choices[0].message.content
    })
    