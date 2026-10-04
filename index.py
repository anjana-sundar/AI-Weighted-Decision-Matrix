import os
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
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path)

app.include_router(ai_router)
