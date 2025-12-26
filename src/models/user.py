from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field
from sqlmodel import SQLModel

from src.utilities.helper import get_utc_now


class UserRole(str, Enum):
    ADMIN = "admin"
    SELLER = "seller"
    CUSTOMER = "customer"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email_id: EmailStr = Field(unique=True, index=True)
    hashed_password: str = Field(nullable=False)
    phone_no: Optional[str] = None
    role: UserRole = Field(default=UserRole.CUSTOMER, index=True)

    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(
        default_factory=get_utc_now, alias="created_at", index=True
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now, alias="updated_at", index=True
    )
