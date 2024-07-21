"""
Public router
"""

from fastapi import APIRouter
from mongodb.models import (MissionUnion, EmbassyDocument, RepresentationDocument,
                            ConsulateDocument)

router = APIRouter()


@router.get("/")
async def all_missions():
    return await MissionUnion.all().to_list()


@router.get("/embassies")
async def all_embassies():
    return await EmbassyDocument.all().to_list()


@router.get("/embassies/{embassy_id}")
async def by_id(embassy_id: str):
    return await EmbassyDocument.get(embassy_id)


@router.get("/representations")
async def all_representations():
    return await RepresentationDocument.all().to_list()


@router.get("/representations/{rep_id}")
async def by_id(rep_id: str):
    return await RepresentationDocument.get(rep_id)


@router.get("/consulates")
async def all_consulates():
    return await ConsulateDocument.all().to_list()


@router.get("/consulates/{consulate_id}")
async def by_id(consulate_id: str):
    return await ConsulateDocument.get(consulate_id)
