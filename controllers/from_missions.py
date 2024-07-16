
from mongodb.mission import MissionUnion
from mongodb.diplomat import DiplomatDocument
import beanie


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
    embassies = [mission for mission in missions if mission.type_of ==
                                                             "embassy"]
    consulates = [mission for mission in missions if mission.type_of == "consulate"]

    for embassy in embassies:
        for consulate in consulates:
            if consulate.contact.country == embassy.host_country.lower():
                embassy.consulates.append(consulate)
    return embassies


async def get_consulates():
    missions = await get_all_missions()
    return [mission for mission in missions if mission.type_of == "consulate"]


async def get_representations():
    missions = await get_all_missions()
    return [mission for mission in missions if mission.type_of == "representation"]


async def get_mission_by_id(mission_id: str) -> beanie.Document:
    missions = await get_all_missions()
    for mission in missions:
        if str(mission.id) == mission_id:
            return mission


async def _get_hom(search_location: str) -> DiplomatDocument:
    diplomats = await DiplomatDocument.all().to_list()

    for diplomat in diplomats:
        if diplomat.mission.lower() == search_location:
            return diplomat
