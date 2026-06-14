from fastapi import APIRouter, HTTPException, Query

from app.schemas.ai import AiAnswerData, AiAskRequest, AiDraftAnswerRequest, AiSource
from app.schemas.common import ApiResponse
from app.services import mock_store


router = APIRouter(prefix="/ai", tags=["ai"])


def search_community(keyword: str) -> list[AiSource]:
    keyword_lower = keyword.lower()
    sources: list[AiSource] = []
    for question in mock_store.questions:
        text = f"{question['title']} {question['content']}".lower()
        tag_text = " ".join(mock_store.tag_names(question["tag_ids"])).lower()
        if keyword_lower in text or keyword_lower in tag_text:
            sources.append(AiSource(type="question", id=question["id"], title=question["title"]))

    for answer in mock_store.answers:
        if keyword_lower in answer["content"].lower():
            question = next((item for item in mock_store.questions if item["id"] == answer["question_id"]), None)
            title = question["title"] if question else f"回答 {answer['id']}"
            sources.append(AiSource(type="answer", id=answer["id"], title=title))

    return sources[:5]


@router.post("/ask", response_model=ApiResponse[AiAnswerData])
def ask_ai(payload: AiAskRequest) -> ApiResponse[AiAnswerData]:
    sources = search_community(payload.question) if payload.use_retrieval else []
    if sources:
        answer = f"已检索到 {len(sources)} 条社区相关内容。建议结合这些来源整理回答：{payload.question}"
    else:
        answer = f"当前为 DeepSeek Flash 接口占位回答。后续接入模型后将回答：{payload.question}"

    return ApiResponse(data=AiAnswerData(answer=answer, sources=sources))


@router.post("/draft-answer", response_model=ApiResponse[AiAnswerData])
def draft_answer(payload: AiDraftAnswerRequest) -> ApiResponse[AiAnswerData]:
    question = next((item for item in mock_store.questions if item["id"] == payload.question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")

    sources = [AiSource(type="question", id=question["id"], title=question["title"])]
    answer = f"回答草稿：针对“{question['title']}”，可以先说明问题背景，再给出步骤和示例。"
    return ApiResponse(data=AiAnswerData(answer=answer, sources=sources))


@router.get("/search", response_model=ApiResponse[list[AiSource]])
def ai_search(keyword: str = Query(min_length=1)) -> ApiResponse[list[AiSource]]:
    return ApiResponse(data=search_community(keyword))

