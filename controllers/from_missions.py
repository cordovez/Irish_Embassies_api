from bson import ObjectId

from mongodb.mission import MissionUnion
from mongodb.diplomat import DiplomatDocument
import beanie


async def _get_hom(search_location: str) -> DiplomatDocument:
    diplomats = await DiplomatDocument.all().to_list()

    for diplomat in diplomats:
        if diplomat.mission.lower() == search_location:
            return diplomat


async def get_all_missions():
    missions = await MissionUnion.all().to_list()

    for mission in missions:
        if mission.type_of == 'embassy':
            mission.head_of_mission = await _get_hom(mission.host_country.lower())
        elif mission.type_of == 'consulate':
            mission.head_of_mission = await _get_hom(mission.host_city.lower())
        elif mission.type_of == 'representation':
            mission.head_of_mission = await _get_hom(mission.representation_name.lower())

    return missions


async def get_embassies():
    missions = await get_all_missions()
    embassies = [mission for mission in missions if mission.type_of == "embassy"]
    consulates = [mission for mission in missions if mission.type_of == "consulate"]

    for embassy in embassies:
        for consulate in consulates:
            if consulate.contact.country == embassy.host_country.lower():
                embassy.consulates.append(consulate)
    return embassies


async def get_consulates():
    missions = await get_all_missions()
    return [mission for mission in missions if mission.type_of == "consulate"]


#TODO: representation is not populating 'head_of_mission'
async def get_representations():
    missions = await get_all_missions()
    return [mission for mission in missions if mission.type_of == "representation"]


async def get_mission_by_id(mission_id: str) -> beanie.Document:
    mission = await MissionUnion.find_one({"_id": ObjectId(mission_id)})
    all_consulates = await get_consulates()
    if mission.type_of == "embassy":
        for consulate in all_consulates:
            if consulate.contact.country.lower() == mission.host_country.lower():
                mission.consulates.append(consulate)

        mission.head_of_mission = await _get_hom(mission.host_country)
    else:
        mission.head_of_mission = await _get_hom(mission.host_city)

    return mission

