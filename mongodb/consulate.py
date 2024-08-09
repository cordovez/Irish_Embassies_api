import pymongo
from mongodb.mission import Mission, MissionUnion


class ConsulateDocument(Mission):
    type_of: str = "consulate"
    host_city: str

    class Settings:
        name = "consulates"
        union_doc = MissionUnion
