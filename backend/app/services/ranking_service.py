from collections import defaultdict

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models.answer import Answer
from app.models.question import Question
from app.models.user import User
from app.schemas.ranking import HotQuestionItem, UserRankingItem


def list_hot_questions(db: Session, limit: int = 10) -> list[HotQuestionItem]:
    questions = db.scalars(
        select(Question)
        .options(selectinload(Question.author), selectinload(Question.tags), selectinload(Question.answers))
        .order_by(Question.created_at.desc())
    ).all()

    ranked = sorted(
        questions,
        key=lambda question: (question.view_count * 2) + (question.like_count * 3) + (len(question.answers) * 5),
        reverse=True,
    )
    items: list[HotQuestionItem] = []
    for question in ranked[:limit]:
        score = (question.view_count * 2) + (question.like_count * 3) + (len(question.answers) * 5)
        items.append(
            HotQuestionItem(
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
    return items


def list_user_rankings(db: Session, limit: int = 10) -> list[UserRankingItem]:
    users = db.scalars(select(User)).all()
    answer_counts = defaultdict(int)
    accepted_counts = defaultdict(int)
    answer_likes = defaultdict(int)

    answers = db.scalars(select(Answer)).all()
    for answer in answers:
        answer_counts[answer.author_id] += 1
        answer_likes[answer.author_id] += answer.like_count
        if answer.is_accepted:
            accepted_counts[answer.author_id] += 1

    ranked = []
    for user in users:
        score = (user.points * 2) + (answer_counts[user.id] * 5) + (accepted_counts[user.id] * 10) + answer_likes[user.id]
        ranked.append(
            UserRankingItem(
                id=user.id,
                username=user.username,
                points=user.points,
                level=user.level,
                answer_count=answer_counts[user.id],
                accepted_count=accepted_counts[user.id],
                like_count=answer_likes[user.id],
                score=score,
            )
        )
    return sorted(ranked, key=lambda item: item.score, reverse=True)[:limit]
