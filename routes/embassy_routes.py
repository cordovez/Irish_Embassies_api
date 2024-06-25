"""
User registration router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from auth.current_user import get_current_user
from mongodb.embassy import EmbassyDocument
from controllers import in_db, in_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create
@router.get("/")
async def all_embassies():
    # await in_db.match_diplomat_to_mission()
    # await in_db.embassy_append_consulates()
    return await EmbassyDocument.all().to_list()


@router.get("/{id}")
async def by_id(id: str):
    # try:
    return await in_collection.embassies_get_populated(id)
    # return await EmbassyDocument.get(id)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
    #     ) from e
