from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.answer import Answer
from app.models.question import Question
from app.models.user import User
from app.schemas.answer import AnswerCreateRequest, AnswerPublic


def _to_answer_public(answer: Answer) -> AnswerPublic:
    return AnswerPublic(
        id=answer.id,
        question_id=answer.question_id,
        content=answer.content,
        author=answer.author.username,
        like_count=answer.like_count,
        is_accepted=answer.is_accepted,
        created_at=answer.created_at,
    )


def list_answers(db: Session, question_id: int) -> list[AnswerPublic]:
    question = db.get(Question, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')

    answers = db.scalars(
        select(Answer)
        .options(selectinload(Answer.author))
        .where(Answer.question_id == question_id)
        .order_by(Answer.created_at.asc())
    ).all()
    return [_to_answer_public(item) for item in answers]


def create_answer(db: Session, question_id: int, author: User, payload: AnswerCreateRequest) -> AnswerPublic:
    question = db.get(Question, question_id)
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Question not found')

    answer = Answer(question_id=question_id, author_id=author.id, content=payload.content)
    db.add(answer)
    db.commit()
    db.refresh(answer)
    answer = db.scalar(select(Answer).options(selectinload(Answer.author)).where(Answer.id == answer.id))
    return _to_answer_public(answer)


def accept_answer(db: Session, answer_id: int, current_user: User) -> AnswerPublic:
    answer = db.scalar(
        select(Answer)
        .options(selectinload(Answer.author), selectinload(Answer.question))
        .where(Answer.id == answer_id)
    )
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Answer not found')
    if answer.question.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only the question author can accept an answer')

    answers = db.scalars(select(Answer).where(Answer.question_id == answer.question_id)).all()
    for item in answers:
        item.is_accepted = item.id == answer.id
    db.commit()
    answer = db.scalar(select(Answer).options(selectinload(Answer.author)).where(Answer.id == answer_id))
    return _to_answer_public(answer)


def like_answer(db: Session, answer_id: int, liked: bool) -> dict:
    answer = db.get(Answer, answer_id)
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Answer not found')
    if liked:
        answer.like_count += 1
    else:
        answer.like_count = max(0, answer.like_count - 1)
    db.commit()
    return {'liked': liked, 'like_count': answer.like_count}
