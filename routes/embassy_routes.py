"""
Embassy router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import from_missions
from mongodb.models import PublicEmbassyDocument

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/")
async def all_embassies():
    return await PublicEmbassyDocument.find().to_list()


@router.get("/{embassy_id}")
async def by_id(embassy_id: str):
    return await PublicEmbassyDocument.get(embassy_id)
