from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from src.db.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        unique=True,
        index=True,
    )
    username = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
