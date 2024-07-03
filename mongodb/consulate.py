import pymongo
from mongodb.mission import Mission, MissionUnion


class ConsulateDocument(Mission):
    type_of: str = "consulate"
    host_city: str

    class Settings:
        name = "consulates"
        union_doc = MissionUnion
        indexes = [
            pymongo.IndexModel(
                keys=[("host_city", pymongo.ASCENDING)], name="consulate_city"
            ),
        ]
