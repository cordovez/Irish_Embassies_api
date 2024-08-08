import pymongo
from mongodb.mission import Mission, MissionUnion
from mongodb.consulate import ConsulateDocument
from schemas.enums import Level
from typing import Optional, List


class EmbassyDocument(Mission):
    type_of: str = "embassy"
    host_country: str
    consulates: Optional[List[ConsulateDocument]] = []
    level: Level = Level.THREE

    class Settings:
        name = "embassies"
        union_doc = MissionUnion
