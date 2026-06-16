from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.question import Question
from app.models.tag import Tag
from app.models.user import User
from app.schemas.question import QuestionCreateRequest, QuestionDetail, QuestionListData, QuestionListItem


def _to_question_item(question: Question) -> QuestionListItem:
    return QuestionListItem(
        id=question.id,
        title=question.title,
        content=question.content,
        author=question.author.username,
        tags=[tag.name for tag in question.tags],
        answer_count=len(question.answers),
        view_count=question.view_count,
        like_count=question.like_count,
        created_at=question.created_at,
    )


def _to_question_detail(question: Question) -> QuestionDetail:
    item = _to_question_item(question)
    return QuestionDetail(**item.model_dump(), is_collected=question.is_collected, collect_count=question.collect_count)


def list_questions(db: Session, keyword: str | None, tag_id: int | None, page: int, page_size: int) -> QuestionListData:
    query = (
        select(Question)
        .options(selectinload(Question.author), selectinload(Question.tags), selectinload(Question.answers))
        .order_by(Question.created_at.desc())
    )
    if keyword:
        pattern = f'%{keyword}%'
        query = query.where((Question.title.ilike(pattern)) | (Question.content.ilike(pattern)))
    if tag_id:
        query = query.join(Question.tags).where(Tag.id == tag_id)

    total_query = select(func.count()).select_from(query.order_by(None).subquery())
    total = db.scalar(total_query) or 0
    items = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()
    return QuestionListData(total=total, items=[_to_question_item(item) for item in items])


def create_question(db: Session, author: User, payload: QuestionCreateRequest) -> QuestionDetail:
    tags = []
    if payload.tag_ids:
        tags = db.scalars(select(Tag).where(Tag.id.in_(payload.tag_ids))).all()

    question = Question(title=payload.title, content=payload.content, author_id=author.id, tags=tags)
    db.add(question)
    db.commit()
    db.refresh(question)
    question = db.scalar(
        select(Question)
        .options(selectinload(Question.author), selectinload(Question.tags), selectinload(Question.answers))
        .where(Question.id == question.id)
    )
    return _to_question_detail(question)


def get_question_or_404(db: Session, question_id: int) -> Question:
    question = db.scalar(
        select(Question)
        .options(selectinload(Question.author), selectinload(Question.tags), selectinload(Question.answers))
        .where(Question.id == question_id)
    )
    if question is None:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')
    return question


def get_question_detail(db: Session, question_id: int) -> QuestionDetail:
    question = get_question_or_404(db, question_id)
    question.view_count += 1
    db.commit()
    db.refresh(question)
    question = get_question_or_404(db, question_id)
    return _to_question_detail(question)


def like_question(db: Session, question_id: int, liked: bool) -> dict:
    question = get_question_or_404(db, question_id)
    if liked:
        question.like_count += 1
    else:
        question.like_count = max(0, question.like_count - 1)
    db.commit()
    return {'liked': liked, 'like_count': question.like_count}


def collect_question(db: Session, question_id: int, collected: bool) -> dict:
    question = get_question_or_404(db, question_id)
    question.is_collected = collected
    question.collect_count = question.collect_count + 1 if collected else max(0, question.collect_count - 1)
    db.commit()
    db.refresh(question)
    return {'collected': collected, 'collect_count': question.collect_count}