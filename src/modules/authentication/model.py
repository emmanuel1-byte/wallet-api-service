from beanie import Document, Indexed
from pydantic import EmailStr, Field
from bson import ObjectId
from typing import Annotated
from datetime import datetime, timezone
from ...enums.enum import Account_status


class User(Document):
    fullname: str
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str
    verified: bool = Field(default=False)
    phone: str
    status: Account_status = Field(default=Account_status.ACTIVE)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"

    class Config:
        arbitrary_types_allowed = True
