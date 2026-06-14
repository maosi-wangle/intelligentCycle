from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas.answer import AnswerCreateRequest, AnswerPublic
from app.schemas.common import ApiResponse
from app.services import mock_store


router = APIRouter(tags=["answers"])


@router.get("/questions/{question_id}/answers", response_model=ApiResponse[list[AnswerPublic]])
def list_answers(question_id: int) -> ApiResponse[list[AnswerPublic]]:
    if not any(item["id"] == question_id for item in mock_store.questions):
        raise HTTPException(status_code=404, detail="问题不存在")
    items = [AnswerPublic(**item) for item in mock_store.answers if item["question_id"] == question_id]
    return ApiResponse(data=items)


@router.post("/questions/{question_id}/answers", response_model=ApiResponse[AnswerPublic], status_code=201)
def create_answer(question_id: int, payload: AnswerCreateRequest) -> ApiResponse[AnswerPublic]:
    question = next((item for item in mock_store.questions if item["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")

    answer = {
        "id": mock_store.next_id(mock_store.answers),
        "question_id": question_id,
        "content": payload.content,
        "author": mock_store.users[0]["username"],
        "like_count": 0,
        "is_accepted": False,
        "created_at": datetime.now(timezone.utc),
    }
    mock_store.answers.append(answer)
    question["answer_count"] += 1
    return ApiResponse(data=AnswerPublic(**answer))


@router.post("/answers/{answer_id}/accept", response_model=ApiResponse[AnswerPublic])
def accept_answer(answer_id: int) -> ApiResponse[AnswerPublic]:
    answer = next((item for item in mock_store.answers if item["id"] == answer_id), None)
    if answer is None:
        raise HTTPException(status_code=404, detail="回答不存在")

    for item in mock_store.answers:
        if item["question_id"] == answer["question_id"]:
            item["is_accepted"] = False
    answer["is_accepted"] = True
    return ApiResponse(data=AnswerPublic(**answer))


@router.post("/answers/{answer_id}/like", response_model=ApiResponse[dict])
def like_answer(answer_id: int) -> ApiResponse[dict]:
    answer = next((item for item in mock_store.answers if item["id"] == answer_id), None)
    if answer is None:
        raise HTTPException(status_code=404, detail="回答不存在")
    answer["like_count"] += 1
    return ApiResponse(data={"liked": True, "like_count": answer["like_count"]})


@router.delete("/answers/{answer_id}/like", response_model=ApiResponse[dict])
def unlike_answer(answer_id: int) -> ApiResponse[dict]:
    answer = next((item for item in mock_store.answers if item["id"] == answer_id), None)
    if answer is None:
        raise HTTPException(status_code=404, detail="回答不存在")
    answer["like_count"] = max(0, answer["like_count"] - 1)
    return ApiResponse(data={"liked": False, "like_count": answer["like_count"]})

