"""
Mission router
"""
from bson import ObjectId
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from controllers import from_missions
from mongodb.models import (EmbassyDocument, MissionUnion, ConsulateDocument,
                            RepresentationDocument)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Todo: all missions are accessible by their Document Model. for example: EmbassyDoc(
#  ).all().to_list() returns all embassies, but unpopulated. The function
#  "from_missions.get_embassies()" will return it populated, but more slowly. Should
#  there be a collection with fixed documents (that is, a collection where all
#  embassies exist with consulates and hom already added?) or am I talking about caching?


@router.get("/")
async def all_missions():
    return await MissionUnion.find().to_list()


@router.get("/embassies")
async def all_mission_embassies():
    return await EmbassyDocument.find().to_list()


@router.get("/consulates/")
async def all_mission_consulates():
    return await ConsulateDocument.find().to_list()


@router.get("/representations/")
async def all_mission_representations():
    return await RepresentationDocument.find().to_list()


@router.get("/{mission_id}")
async def by_id(mission_id: str):
    return await MissionUnion.find_one({"_id": ObjectId(mission_id)})


@router.get("/create")
async def create_mission():
    return {"message": "route not yet implemented"}


@router.post("/{mission_id}/update")
async def update_mission(mission_id: str):
    return {"message": "route not yet implemented"}


@router.post("/{mission_id}/delete")
async def delete_mission(mission_id: str):
    return {"message": "route not yet implemented"}
