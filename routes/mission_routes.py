"""
Mission router
"""
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from mongodb.models import (MissionUnion)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/")
async def all_missions():
    return await MissionUnion.find().to_list()
