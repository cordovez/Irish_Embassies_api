"""
Public router
"""

from fastapi import APIRouter, HTTPException, status

from controllers.from_db import pydantic_response_for_all_items, \
    pydantic_response_for_one_item
from mongodb.models import (MissionUnion, EmbassyDocument, RepresentationDocument,
                            ConsulateDocument, CountryDocument, DiplomatDocument)
from schemas.pydantic_schemas import (DiplomatOut, EmbassyOut, ConsulateOut,
                                      RepresentationOut, CountryOut)

router = APIRouter()


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


@router.get("/diplomats/", response_model=list[DiplomatOut])
async def all_diplomats():
    response = await DiplomatDocument.all().to_list()
    homs = pydantic_response_for_all_items(response, DiplomatOut)
    return sorted(homs, key=lambda x: x.last_name)


@router.get("/diplomats/{diplomat_id}", response_model=DiplomatOut)
async def consulate_by_id(diplomat_id: str):
    response = await DiplomatDocument.get(diplomat_id)
    return pydantic_response_for_one_item(response, DiplomatOut)


@router.get("/countries")
async def all_countries():
    response = await CountryDocument.all().to_list()
    return pydantic_response_for_all_items(response, CountryOut)

@router.get("/countries/{country_id}")
async def by_id(country_id: str):
    try:
        return await CountryDocument.get(country_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            ) from e
