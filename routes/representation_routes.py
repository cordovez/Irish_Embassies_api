import fastapi
from fastapi import HTTPException, status
from mongodb.representation import RepresentationDocument
from controllers import in_collection


router = fastapi.APIRouter()


@router.get("/")
async def all_representations():
    return await RepresentationDocument.find().to_list()


@router.get("/{id}")
async def by_id(id: str):
    return await in_collection.representations_add_head_of_mission(id)
