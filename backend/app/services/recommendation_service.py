from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.question import Question
from app.models.tag import Tag
from app.models.user import User
from app.schemas.recommendation import RecommendationItem


def recommend_questions(db: Session, current_user: User | None = None, limit: int = 10) -> list[RecommendationItem]:
    questions = db.scalars(
        select(Question)
        .options(selectinload(Question.author), selectinload(Question.tags), selectinload(Question.answers))
        .order_by(Question.created_at.desc())
    ).all()

    preferred_tag_ids: set[int] = set()
    if current_user is not None:
        preferred_tag_ids = {
            tag.id
            for question in questions
            for tag in question.tags
            if question.author_id == current_user.id
        }

    ranked = []
    for question in questions:
        tag_bonus = sum(6 for tag in question.tags if tag.id in preferred_tag_ids)
        score = (question.like_count * 3) + (len(question.answers) * 4) + question.view_count + tag_bonus
        ranked.append(
            RecommendationItem(
                id=question.id,
                title=question.title,
                author=question.author.username,
                tags=[tag.name for tag in question.tags],
                answer_count=len(question.answers),
                view_count=question.view_count,
                like_count=question.like_count,
                score=score,
                created_at=question.created_at,
            )
        )
    return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]
