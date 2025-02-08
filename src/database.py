from sqlalchemy import TIMESTAMP, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql.expression import text
from datetime import datetime
from config import settings

class Base(DeclarativeBase):
    pass

class Questions(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String(200))
    answer: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    def __repr__(self) -> str:
        return f"Question(id={self.id}, question={self.question}, answer={self.answer}, created_at={self.created_at})"


engine = create_async_engine(settings.postgres_url)
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with new_session() as session:
        yield session
