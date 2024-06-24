"""
User registration router
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from auth.current_user import get_current_user
from mongodb.embassy import EmbassyDocument

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


# Create
@router.get("/")
async def all_embassies():
    return await EmbassyDocument.find().to_list()


@router.get("/{id}")
async def by_id(id: str):
    try:
        return await EmbassyDocument.get(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        ) from e
