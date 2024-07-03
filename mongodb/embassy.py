import pymongo
from mongodb.mission import Mission, MissionUnion
from mongodb.consulate import ConsulateDocument
from schemas.enums import Level
from typing import Optional, List
from beanie import Link


class EmbassyDocument(Mission):
    type_of: str = "embassy"
    host_country: str
    consulates: Optional[List[Link[ConsulateDocument]]] = []
    level: Level = Level.THREE

    class Settings:
        name = "embassies"
        union_doc = MissionUnion
        indexes = [
            pymongo.IndexModel(
                keys=[("host_country", pymongo.ASCENDING)],
                name="embassy_ascending",
            ),
        ]
