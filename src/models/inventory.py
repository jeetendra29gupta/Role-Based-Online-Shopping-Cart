from datetime import datetime
from typing import Optional

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

from src.utilities.helper import get_utc_now


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = Field(default=None)
    price: float = Field(nullable=False, gt=0)
    quantity: int = Field(default=0, ge=0)
    image: Optional[str] = Field(default=None)

    # Foreign Key to User (Seller)
    seller_id: int = Field(foreign_key="users.id", nullable=False)
    seller: Optional["User"] = Relationship(  # noqa
        sa_relationship_kwargs={"lazy": "select"},  # lazy loading
        back_populates=None,  # one-directional
    )

    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(
        default_factory=get_utc_now, alias="created_at", index=True
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now, alias="updated_at", index=True
    )
