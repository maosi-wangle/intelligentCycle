from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ai, answers, auth, questions, rankings, recommendations, tags, users
from app.core.config import settings
from app.schemas.common import ApiResponse


app = FastAPI(
    title=settings.app_name,
    description="智答圈后端接口，供 Vue 前端对接使用。",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=ApiResponse[dict])
def health_check() -> ApiResponse[dict]:
    return ApiResponse(data={"status": "ok", "docs": "/docs"})


app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(questions.router, prefix=settings.api_prefix)
app.include_router(answers.router, prefix=settings.api_prefix)
app.include_router(tags.router, prefix=settings.api_prefix)
app.include_router(rankings.router, prefix=settings.api_prefix)
app.include_router(recommendations.router, prefix=settings.api_prefix)
app.include_router(ai.router, prefix=settings.api_prefix)

