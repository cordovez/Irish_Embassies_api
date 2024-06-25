import fastapi
from fastapi import HTTPException, status
from mongodb.consulate import ConsulateDocument
from controllers import in_collection


router = fastapi.APIRouter()


@router.get("/")
async def all_consulates():
    return await ConsulateDocument.find().to_list()


@router.get("/{id}")
async def by_id(id: str):
    return await in_collection.consulates_add_head_of_mission(id)
