import secrets
from sqlmodel import Field, Relationship

from nexura.models.base import BaseWithDeleted


def generate_apikey() -> str:
    return secrets.token_urlsafe(32)


class APIKey(BaseWithDeleted, table=True):
    key: str = Field(default=generate_apikey, primary_key=True)

    user_id: str = Field(foreign_key="user.id")
    user = Relationship(back_populates="api_keys")
