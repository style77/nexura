import datetime
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    created_at = Field(default=datetime.datetime.utcnow)
    updated_at = Field(default=datetime.datetime.utcnow)


class BaseWithDeleted(Base):
    deleted_at = Field(default=None)


class BaseWithID(Base):
    id: int = Field(default=None, primary_key=True)
