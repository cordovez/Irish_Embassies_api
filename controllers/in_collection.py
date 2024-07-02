import asyncio

from fastapi import HTTPException
from beanie import WriteRules

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

    populated_embassies = await asyncio.gather(
        *[populate_embassy(embassy) for embassy in embassies])
    return populated_embassies


async def embassies_get_populated(emb_id: str) -> EmbassyDocument:
    embassy = await EmbassyDocument.get(emb_id)
    if not embassy:
        raise HTTPException(status_code=404, detail="Embassy not found")

    country = embassy.host_country.lower()
    if not embassy.head_of_mission:
        embassy.head_of_mission = await _find_head_of_mission(country)

    # if len(embassy.consulates ) == 0:
    #     consulates = []
    #     for cons in await ConsulateDocument.all().to_list():
    #         consulate_country = cons.contact.country.lower()
    #         mission = cons.host_city.lower()
    #         diplomat = await _find_head_of_mission(mission)
    #         cons.head_of_mission = diplomat.id
    #         if consulate_country == country:
    #             consulates.append(cons)
    #             embassy.consulates = consulates

    return embassy


async def consulates_add_head_of_mission(cons_id: str) -> ConsulateDocument:
    consulate = await ConsulateDocument.get(cons_id)
    if not consulate:
        raise HTTPException(status_code=404, detail="Embassy not found")

    city = consulate.host_city.lower()
    diplomat = await _find_head_of_mission(city)
    consulate.head_of_mission = diplomat.id

    return consulate


async def representations_add_head_of_mission(rep_id: str) -> RepresentationDocument:
    rep = await RepresentationDocument.get(rep_id)
    if not rep:
        raise HTTPException(status_code=404, detail="Embassy not found")

    name = rep.representation_name.lower()
    diplomat = await _find_head_of_mission(name)
    rep.head_of_mission = diplomat.id

    return rep

# TODO: Add an admin route that uses the missions_populate before returning all embassies

async def missions_populate() -> None:
    await _assign_heads_of_mission()
    embassies = await EmbassyDocument.all().to_list()

    for embassy in embassies:
        consulates = await _match_consulates_to_embassy(embassy.host_country)
        await embassy.save(link_rule=WriteRules.WRITE)


async def _match_consulates_to_embassy(country:str)->list[ConsulateDocument]:
    consulates = []
    for cons in await ConsulateDocument.all().to_list():
        consulate_country = cons.contact.country.lower()
        if consulate_country == country:
            consulates.append(cons)
    return consulates


async def _find_head_of_mission(mission_name: str) -> DiplomatDocument:
    for dip in await DiplomatDocument.all().to_list():
        dip.mission = dip.mission.lower()
        if dip.mission == mission_name:
            return dip


async def _assign_heads_of_mission() -> None:
    consulates = await ConsulateDocument.all().to_list()
    reps = await RepresentationDocument.all().to_list()
    embassies = await EmbassyDocument.all().to_list()

    for consulate in consulates:
        mission = consulate.host_city.lower()
        assigned_dip = await _find_head_of_mission(mission)
        await consulate.save(link_rule=WriteRules.WRITE)

    for rep in reps:
        mission = rep.representation_name.lower()
        assigned_dip = await _find_head_of_mission(mission)
        await rep.save(link_rule=WriteRules.WRITE)

    for embassy in embassies:
        mission = embassy.host_country.lower()
        assigned_dip = await _find_head_of_mission(mission)
        await embassy.save(link_rule=WriteRules.WRITE)

