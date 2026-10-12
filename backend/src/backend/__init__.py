from backend.core.database import Base, engine
from backend.domain.users.models.user import User  # noqa: F401


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print("Hello from backend!")
