from fastapi import FastAPI
from routes.ai_routes import router as ai_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Weighted Decision Matrix API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "success": True,
        "message": "API is running"
    }

app.include_router(ai_router)