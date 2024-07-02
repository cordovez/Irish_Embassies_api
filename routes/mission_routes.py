"""
Mission router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import from_missions
from controllers import in_collection
from mongodb.mission import MissionUnion

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create


@router.get("/")
async def all_missions():
    # return await in_collection.embassies_query_all()
    # return await in_collection.embassies_return_all()
    return await from_missions.get_all_missions()
    # return await MissionUnion.all().to_list()


@router.get("/{id}")
async def by_id(mission_id: str):
    pass
    # return await in_collection...(mission_id)
