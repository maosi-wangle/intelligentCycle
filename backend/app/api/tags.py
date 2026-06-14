from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import ApiResponse
from app.schemas.tag import TagCreateRequest, TagPublic
from app.services.tag_service import create_tag, list_tags


router = APIRouter(prefix='/tags', tags=['tags'])


@router.get('', response_model=ApiResponse[list[TagPublic]])
def get_tags(db: Session = Depends(get_db)) -> ApiResponse[list[TagPublic]]:
    return ApiResponse(data=list_tags(db))


@router.post('', response_model=ApiResponse[TagPublic], status_code=201)
def post_tag(payload: TagCreateRequest, db: Session = Depends(get_db)) -> ApiResponse[TagPublic]:
    return ApiResponse(data=create_tag(db, payload))
