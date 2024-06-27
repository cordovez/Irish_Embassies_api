import asyncio
from fastapi import HTTPException, status
from typing import Optional
from beanie import UpdateResponse

from mongodb.models import (
    EmbassyDocument,
    ConsulateDocument,
    DiplomatDocument,
    RepresentationDocument,
)


async def embassies_return_all():
    embassies = await EmbassyDocument.all().to_list()

    async def populate_embassy(embassy):
        return await embassies_get_populated(embassy.id)

    populated_embassies = await asyncio.gather(*[populate_embassy(embassy) for embassy in embassies])
    return populated_embassies


async def embassies_get_populated(emb_id: str) -> EmbassyDocument:
    embassy = await EmbassyDocument.get(emb_id)
    if not embassy:
        raise HTTPException(status_code=404, detail="Embassy not found")

    country = embassy.host_country.lower()
    embassy.head_of_mission = await _find_head_of_mission(country)

    consulates = []
    for cons in await ConsulateDocument.all().to_list():
        consulate_country = cons.contact.country.lower()
        mission = cons.host_city.lower()
        cons.head_of_mission = await _find_head_of_mission(mission)
        if consulate_country == country:
            consulates.append(cons)
            embassy.consulates = consulates

    return embassy


async def consulates_add_head_of_mission(cons_id: str) -> ConsulateDocument:
    consulate = await ConsulateDocument.get(cons_id)
    if not consulate:
        raise HTTPException(status_code=404, detail="Embassy not found")

    city = consulate.host_city.lower()
    consulate.head_of_mission = await _find_head_of_mission(city)

    return consulate


async def representations_add_head_of_mission(rep_id: str) -> RepresentationDocument:
    rep = await RepresentationDocument.get(rep_id)
    if not rep:
        raise HTTPException(status_code=404, detail="Embassy not found")

    name = rep.representation_name.lower()
    rep.head_of_mission = await _find_head_of_mission(name)

    return rep


async def _find_head_of_mission(mission_name: str) -> DiplomatDocument:
    for dip in await DiplomatDocument.all().to_list():
        dip.mission = dip.mission.lower()
        if dip.mission == mission_name:
            return dip
