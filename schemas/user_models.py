"""
User Models
"""

# import pytz
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


# central_europe = pytz.timezone('Europe/Paris')


class ImageBase(BaseModel):
    public_id: str
    uri: str


class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    avatar: dict
    email: EmailStr
    username: str
    created_at: datetime


class UserUpdate(BaseModel):
    """User database representation"""

    model_config = ConfigDict(extra="allow")

    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    username: Optional[str] | None = None
