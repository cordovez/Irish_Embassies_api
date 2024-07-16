"""
Mission router
"""

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import from_missions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Todo: all missions are accessible by their Document Model. for example: EmbassyDoc(
#  ).all().to_list() returns all embassies, but unpopulated. The function
#  "from_missions.get_embassies()" will return it populated, but more slowly. Should
#  there be a collection with fixed documents (that is, a collection where all
#  embassies exist with consulates and hom already added?) or am I talking about caching?



@router.get("/")
async def all_missions():
    # return await in_collection.embassies_query_all()
    # return await in_collection.embassies_return_all()
    return await from_missions.get_all_missions()
    # return await MissionUnion.all().to_list()


@router.get("/{mission_id}")
async def by_id(mission_id: str):

    return await from_missions.get_mission_by_id(mission_id)
