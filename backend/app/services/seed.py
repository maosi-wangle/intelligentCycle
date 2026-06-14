from sqlalchemy import select

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.answer import Answer
from app.models.question import Question
from app.models.tag import Tag
from app.models.user import User


def seed_data() -> None:
    db = SessionLocal()
    try:
        if db.scalar(select(User).where(User.username == 'student01')) is not None:
            return

        user = User(
            username='student01',
            email='student01@example.com',
            password_hash=hash_password('123456'),
            points=120,
            level=3,
        )
        db.add(user)
        db.flush()

        tag_fastapi = Tag(name='FastAPI', description='Python Web backend framework')
        tag_jwt = Tag(name='JWT', description='User authentication token')
        tag_vue = Tag(name='Vue', description='Frontend framework')
        db.add_all([tag_fastapi, tag_jwt, tag_vue])
        db.flush()

        question = Question(
            title='How to implement JWT login in FastAPI?',
            content='I want to build login and auth flow in FastAPI. What is the common practice?',
            author_id=user.id,
            view_count=30,
            like_count=5,
            tags=[tag_fastapi, tag_jwt],
        )
        db.add(question)
        db.flush()

        answer = Answer(
            question_id=question.id,
            author_id=user.id,
            content='You can use OAuth2PasswordBearer and return a signed JWT access token.',
            like_count=3,
            is_accepted=True,
        )
        db.add(answer)
        db.commit()
    finally:
        db.close()
