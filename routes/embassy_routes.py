"""
User registration router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from auth.current_user import get_current_user
from mongodb.embassy import EmbassyDocument
from controllers import in_collection

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create
@router.get("/")
async def all_embassies():
    return await in_collection.embassies_return_all()

    # return await EmbassyDocument.all().to_list()


@router.get("/{id}")
async def by_id(id: str):
    return await in_collection.embassies_get_populated(id)
