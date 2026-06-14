from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tag import Tag
from app.schemas.tag import TagCreateRequest, TagPublic


def list_tags(db: Session) -> list[TagPublic]:
    tags = db.scalars(select(Tag).order_by(Tag.name.asc())).all()
    return [TagPublic(id=tag.id, name=tag.name, description=tag.description) for tag in tags]


def create_tag(db: Session, payload: TagCreateRequest) -> TagPublic:
    existing = db.scalar(select(Tag).where(Tag.name == payload.name))
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Tag already exists')

    tag = Tag(name=payload.name, description=payload.description)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return TagPublic(id=tag.id, name=tag.name, description=tag.description)
