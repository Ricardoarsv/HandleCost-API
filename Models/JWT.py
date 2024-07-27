from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[int]


class TokenData(BaseModel):
    username: str | None = None
