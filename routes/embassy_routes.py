"""
Embassy router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import in_collection, from_missions
from mongodb.mission import MissionUnion

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create


@router.get("/")
async def all_embassies():
    # return await in_collection.embassies_query_all()
    # return await in_collection.embassies_return_all()

    return await from_missions.get_embassies()


@router.get("/{id}")
async def by_id(embassy_id: str):
    return await from_missions.get_mission_by_id(embassy_id)
