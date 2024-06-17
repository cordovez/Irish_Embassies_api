import datetime

import beanie
from pydantic import ConfigDict, EmailStr
from typing import Optional
import pytz
from datetime import datetime
import pymongo

central_europe = pytz.timezone("Europe/Paris")


class UserBase(beanie.Document):
    """User database representation"""

    model_config = ConfigDict(extra="allow")

    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    created_at: Optional[datetime] = datetime.now(central_europe)
    disabled: bool = False
    email: Optional[EmailStr] | None = None
    username: Optional[str] | None = None
    password_hash: Optional[str] | None = None

    class Settings:
        name = "users"
        indexes = [
            pymongo.IndexModel(
                keys=[("username", pymongo.ASCENDING)], name="username_ascend"
            ),
            pymongo.IndexModel(
                keys=[("last_name", pymongo.ASCENDING)], name="lastname_ascend"
            ),
        ]


# class User(beanie.Document):
#     created_date: datetime.datetime = pydantic.Field(
#         default_factory=datetime.datetime.now
#     )
#     last_login: datetime.datetime = pydantic.Field(
#         default_factory=datetime.datetime.now
#     )

#     name: str
#     email: str
#     # password_hash: str
#     # is_admin: bool = False

#     class Settings:
#         name = "users"
#         use_revision = False
#         indexes = [
#             pymongo.IndexModel(
#                 keys=[("created_date", pymongo.ASCENDING)], name="created_date_ascend"
#             ),
#             pymongo.IndexModel(
#                 keys=[("last_updated", pymongo.DESCENDING)],
#                 name="last_updated_descending",
#             ),
#             pymongo.IndexModel(
#                 keys=[("email", pymongo.ASCENDING)], name="email_ascend", unique=True
#             ),
#         ]
