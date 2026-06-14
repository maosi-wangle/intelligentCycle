from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.tag import TagCreateRequest, TagPublic
from app.services import mock_store


router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("", response_model=ApiResponse[list[TagPublic]])
def list_tags() -> ApiResponse[list[TagPublic]]:
    return ApiResponse(data=[TagPublic(**item) for item in mock_store.tags])


@router.post("", response_model=ApiResponse[TagPublic], status_code=201)
def create_tag(payload: TagCreateRequest) -> ApiResponse[TagPublic]:
    tag = {
        "id": mock_store.next_id(mock_store.tags),
        "name": payload.name,
        "description": payload.description,
    }
    mock_store.tags.append(tag)
    return ApiResponse(data=TagPublic(**tag))

