from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from backend.core.database import Base

# [요구사항]

class UserProfile(Base):
    __tablename__ = 'user_profiles'


