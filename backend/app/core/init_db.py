from app.core.database import Base, engine
from app.models import answer, question, tag, user  # noqa: F401
from app.services.seed import seed_data


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    seed_data()
