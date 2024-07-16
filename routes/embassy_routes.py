"""
Embassy router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import from_missions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/")
async def all_embassies():
    # return await EmbassyDocument.all().to_list()
    return await from_missions.get_embassies()


@router.get("/{embassy_id}")
async def by_id(embassy_id: str):
    return await from_missions.get_mission_by_id(embassy_id)
