from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Query

from app.schemas.common import ApiResponse
from app.schemas.question import QuestionCreateRequest, QuestionDetail, QuestionListData, QuestionListItem
from app.services import mock_store


router = APIRouter(prefix="/questions", tags=["questions"])


def to_question_item(question: dict) -> QuestionListItem:
    return QuestionListItem(
        id=question["id"],
        title=question["title"],
        content=question["content"],
        author=question["author"],
        tags=mock_store.tag_names(question["tag_ids"]),
        answer_count=question["answer_count"],
        view_count=question["view_count"],
        like_count=question["like_count"],
        created_at=question["created_at"],
    )


@router.get("", response_model=ApiResponse[QuestionListData])
def list_questions(
    keyword: str | None = None,
    tag_id: int | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
) -> ApiResponse[QuestionListData]:
    items = mock_store.questions
    if keyword:
        items = [
            item
            for item in items
            if keyword.lower() in item["title"].lower() or keyword.lower() in item["content"].lower()
        ]
    if tag_id:
        items = [item for item in items if tag_id in item["tag_ids"]]

    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    page_items = [to_question_item(item) for item in items[start:end]]
    return ApiResponse(data=QuestionListData(total=total, items=page_items))


@router.post("", response_model=ApiResponse[QuestionDetail], status_code=201)
def create_question(payload: QuestionCreateRequest) -> ApiResponse[QuestionDetail]:
    question = {
        "id": mock_store.next_id(mock_store.questions),
        "title": payload.title,
        "content": payload.content,
        "author": mock_store.users[0]["username"],
        "tag_ids": payload.tag_ids,
        "answer_count": 0,
        "view_count": 0,
        "like_count": 0,
        "created_at": datetime.now(timezone.utc),
        "is_collected": False,
    }
    mock_store.questions.append(question)
    return ApiResponse(data=QuestionDetail(**to_question_item(question).model_dump(), is_collected=False))


@router.get("/{question_id}", response_model=ApiResponse[QuestionDetail])
def get_question(question_id: int) -> ApiResponse[QuestionDetail]:
    question = next((item for item in mock_store.questions if item["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")

    question["view_count"] += 1
    return ApiResponse(
        data=QuestionDetail(
            **to_question_item(question).model_dump(),
            is_collected=question["is_collected"],
        )
    )


@router.post("/{question_id}/like", response_model=ApiResponse[dict])
def like_question(question_id: int) -> ApiResponse[dict]:
    question = next((item for item in mock_store.questions if item["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")
    question["like_count"] += 1
    return ApiResponse(data={"liked": True, "like_count": question["like_count"]})


@router.delete("/{question_id}/like", response_model=ApiResponse[dict])
def unlike_question(question_id: int) -> ApiResponse[dict]:
    question = next((item for item in mock_store.questions if item["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")
    question["like_count"] = max(0, question["like_count"] - 1)
    return ApiResponse(data={"liked": False, "like_count": question["like_count"]})


@router.post("/{question_id}/collect", response_model=ApiResponse[dict])
def collect_question(question_id: int) -> ApiResponse[dict]:
    question = next((item for item in mock_store.questions if item["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")
    question["is_collected"] = True
    return ApiResponse(data={"collected": True})


@router.delete("/{question_id}/collect", response_model=ApiResponse[dict])
def uncollect_question(question_id: int) -> ApiResponse[dict]:
    question = next((item for item in mock_store.questions if item["id"] == question_id), None)
    if question is None:
        raise HTTPException(status_code=404, detail="问题不存在")
    question["is_collected"] = False
    return ApiResponse(data={"collected": False})

