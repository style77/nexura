from sqlmodel import Field, Relationship
from nexura.models.api_key import APIKey

from nexura.models.base import Base


class User(Base):
    id = Field(default=None, primary_key=True)

    api_keys: list[APIKey] = Relationship(back_populates="user")
