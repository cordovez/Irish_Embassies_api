"""
Public router
"""

from fastapi import APIRouter

from controllers.from_db import pydantic_response_for_all_items, \
    pydantic_response_for_one_item
from mongodb.models import (MissionUnion, EmbassyDocument, RepresentationDocument,
                            ConsulateDocument)
from schemas.pydantic_schemas import EmbassyOut, ConsulateOut, RepresentationOut

router = APIRouter()


# TODO: return item ids
@router.get("/")
async def all_missions():
    return await MissionUnion.all().to_list()


@router.get("/embassies", response_model=list[EmbassyOut])
async def all_embassies():
    response = await EmbassyDocument.all().to_list()
    embassies = pydantic_response_for_all_items(response, EmbassyOut)
    return sorted(embassies, key=lambda x: x.country)


@router.get("/embassies/{embassy_id}", response_model=EmbassyOut)
async def embassy_by_id(embassy_id: str):
    response = await EmbassyDocument.get(embassy_id)
    return pydantic_response_for_one_item(response, EmbassyOut)


@router.get("/representations", response_model=list[RepresentationOut])
async def all_representations():
    response = await RepresentationDocument.all().to_list()
    representations = pydantic_response_for_all_items(response, RepresentationOut)
    return sorted(representations, key=lambda x: x.rep_name)


@router.get("/representations/{rep_id}")
async def rep_by_id(rep_id: str):
    response = await RepresentationDocument.get(rep_id)
    return pydantic_response_for_one_item(response, RepresentationOut)


@router.get("/consulates")
async def all_consulates():
    response = await ConsulateDocument.all().to_list()
    consulates = pydantic_response_for_all_items(response, ConsulateOut)
    return sorted(consulates, key=lambda x: x.city)


@router.get("/consulates/{consulate_id}")
async def consulate_by_id(consulate_id: str):
    response = await ConsulateDocument.get(consulate_id)
    return pydantic_response_for_one_item(response, ConsulateOut)
