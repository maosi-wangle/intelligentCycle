from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.answer import Answer
from app.models.question import Question
from app.models.tag import Tag
from app.schemas.ai import AiSource


def search_questions(db: Session, keyword: str, limit: int = 5) -> list[AiSource]:
    pattern = f'%{keyword}%'
    questions = db.scalars(
        select(Question)
        .options(selectinload(Question.tags))
        .where((Question.title.ilike(pattern)) | (Question.content.ilike(pattern)))
        .order_by(Question.like_count.desc(), Question.view_count.desc())
        .limit(limit)
    ).all()
    return [
        AiSource(
            type='question',
            id=question.id,
            title=question.title,
            snippet=question.content[:180],
        )
        for question in questions
    ]


def search_answers(db: Session, keyword: str, limit: int = 5) -> list[AiSource]:
    pattern = f'%{keyword}%'
    answers = db.scalars(
        select(Answer)
        .options(selectinload(Answer.question))
        .where(Answer.content.ilike(pattern))
        .order_by(Answer.like_count.desc(), Answer.created_at.desc())
        .limit(limit)
    ).all()
    return [
        AiSource(
            type='answer',
            id=answer.id,
            title=answer.question.title if answer.question else f'Answer #{answer.id}',
            snippet=answer.content[:180],
        )
        for answer in answers
    ]


def search_tags(db: Session, keyword: str, limit: int = 5) -> list[AiSource]:
    pattern = f'%{keyword}%'
    tags = db.scalars(
        select(Tag)
        .where((Tag.name.ilike(pattern)) | (Tag.description.ilike(pattern)))
        .order_by(Tag.name.asc())
        .limit(limit)
    ).all()
    return [
        AiSource(
            type='tag',
            id=tag.id,
            title=tag.name,
            snippet=tag.description,
        )
        for tag in tags
    ]


def get_question_context(db: Session, question_id: int) -> tuple[str, list[AiSource]]:
    question = db.scalar(
        select(Question)
        .options(selectinload(Question.answers), selectinload(Question.tags))
        .where(Question.id == question_id)
    )
    if question is None:
        raise ValueError('Question not found')

    sources = [
        AiSource(
            type='question',
            id=question.id,
            title=question.title,
            snippet=question.content[:180],
        )
    ]
    answer_lines = []
    for answer in question.answers[:5]:
        answer_lines.append(f'- Answer #{answer.id}: {answer.content}')
        sources.append(
            AiSource(
                type='answer',
                id=answer.id,
                title=question.title,
                snippet=answer.content[:180],
            )
        )

    tags = ', '.join(tag.name for tag in question.tags)
    context = f'Title: {question.title}\nTags: {tags}\nContent: {question.content}\nExisting Answers:\n' + '\n'.join(answer_lines)
    return context, sources


def retrieve_context(db: Session, keyword: str) -> tuple[str, list[AiSource]]:
    sources: list[AiSource] = []
    sources.extend(search_questions(db, keyword, limit=3))
    sources.extend(search_answers(db, keyword, limit=3))
    sources.extend(search_tags(db, keyword, limit=2))

    deduped = []
    seen = set()
    for source in sources:
        key = (source.type, source.id)
        if key not in seen:
            seen.add(key)
            deduped.append(source)

    context_lines = []
    for source in deduped:
        snippet = source.snippet or ''
        context_lines.append(f'[{source.type}:{source.id}] {source.title}\n{snippet}')
    return '\n\n'.join(context_lines), deduped
