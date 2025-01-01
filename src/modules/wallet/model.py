from beanie import Document, Indexed, Link
from pydantic import Field
from typing import Annotated
from datetime import datetime, timezone

from src import User
from ...enums.enum import Wallet_status


class Wallet(Document):
    user: Annotated[Link[User], Indexed(unique=True)]
    balance: int = Field(default=0)
    spending_limit: int = Field(default=0)
    pin: Annotated[str, Indexed(unique=True)] = Field(default="")
    account_name: Annotated[str, Indexed(unique=True)] = Field(default="")
    account_number: Annotated[str, Indexed(unique=True)] = Field(default="")
    status: Wallet_status = Field(default=Wallet_status.UNFROZEN)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "wallet"

    class Config:
        arbitrary_types_allowed = True
