from sqlalchemy import Column, String, text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from stock_analysis.db.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        unique=True,
        index=True,
    )
    user_name = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    __table_args__ = (
        UniqueConstraint("email"),
        UniqueConstraint("user_name"),
    )
