from fastapi import HTTPException, status

from beanie import UpdateResponse

from auth.password_hasher import get_password_hash
from mongodb.models import (
    EmbassyDocument,
    ConsulateDocument,
    DiplomatDocument,
)
from schemas.enums import MissionType
from controllers import in_db


async def embassies_get_populated(id: str):
    embassy = await EmbassyDocument.get(id)
    country = embassy.host_country.lower()

    if not embassy:
        raise HTTPException(status_code=404, detail="Embassy not found")

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


async def _find_head_of_mission(mission_name: str) -> DiplomatDocument:
    for dip in await DiplomatDocument.all().to_list():
        dip.mission = dip.mission.lower()
        if dip.mission == mission_name:
            return dip
