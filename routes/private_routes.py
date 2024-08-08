"""
Private router
"""

from fastapi import APIRouter, HTTPException
from schemas.pydantic_schemas import RepresentationIn, DiplomatIn
from mongodb.models import RepresentationDocument, DiplomatDocument

router = APIRouter()


@router.post("/representations/{rep_id}")
async def update_representation(request: RepresentationIn, rep_id: str):
    found_rep = await RepresentationDocument.get(rep_id)
    if not found_rep:
        raise HTTPException(status_code=404, detail="Representation not found")

    update_data = request.model_dump(exclude_unset=True)
    await found_rep.set(update_data)
    return found_rep


@router.put("/diplomats/create")
async def add_diplomat(request: DiplomatIn):
    create_data = request.model_dump(exclude_unset=True)
    diplomat = DiplomatDocument(**create_data)

    return await diplomat.create()


@router.put("/representations/create")
async def add_representation(request: RepresentationIn):
    create_data = request.model_dump(exclude_unset=True)
    rep = RepresentationDocument(**create_data)
    return await rep.create()
