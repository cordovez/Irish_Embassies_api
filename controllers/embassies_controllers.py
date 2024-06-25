from fastapi import HTTPException, status

from beanie import UpdateResponse

from auth.password_hasher import get_password_hash
from mongodb.models import (
    EmbassyDocument,
    ConsulateDocument,
    DiplomatDocument,
)
from schemas.enums import MissionType
