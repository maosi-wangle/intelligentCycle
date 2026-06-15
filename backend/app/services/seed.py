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

        user1 = User(
            username='student01',
            email='student01@example.com',
            password_hash=hash_password('123456'),
            points=1200,
            level=10,
        )
        user2 = User(
            username='teacher01',
            email='teacher01@example.com',
            password_hash=hash_password('123456'),
            points=850,
            level=8,
        )
        user3 = User(
            username='admin',
            email='admin@example.com',
            password_hash=hash_password('123456'),
            points=2000,
            level=15,
        )
        user4 = User(
            username='guest',
            email='guest@example.com',
            password_hash=hash_password('123456'),
            points=500,
            level=5,
        )
        user5 = User(
            username='developer',
            email='developer@example.com',
            password_hash=hash_password('123456'),
            points=1500,
            level=12,
        )
        db.add_all([user1, user2, user3, user4, user5])
        db.flush()

        tag_fastapi = Tag(name='FastAPI', description='Python Web backend framework')
        tag_jwt = Tag(name='JWT', description='User authentication token')
        tag_vue = Tag(name='Vue', description='Frontend framework')
        db.add_all([tag_fastapi, tag_jwt, tag_vue])
        db.flush()

        question = Question(
            title='How to implement JWT login in FastAPI?',
            content='I want to build login and auth flow in FastAPI. What is the common practice?',
            author_id=user1.id,
            view_count=30,
            like_count=5,
            tags=[tag_fastapi, tag_jwt],
        )
        db.add(question)
        db.flush()

        answer = Answer(
            question_id=question.id,
            author_id=user1.id,
            content='You can use OAuth2PasswordBearer and return a signed JWT access token.',
            like_count=3,
            is_accepted=True,
        )
        db.add(answer)
        db.commit()
    finally:
        db.close()